package game

import (
	"log"
	"sync"
	"time"
)

// Keep track of number of active game engines (should only be one)
var activeGameEngines = 0

// Mutex to protect numActiveGameEngines
var muAGE sync.Mutex

/*
A game engine object, to act as an intermediary between the web broker
and the internal game state - its responsibility is to read responses from
clients and routinely send serialized copies of the game state to them
*/
type GameEngine struct {
	quitCh      chan struct{}
	webOutputCh chan<- []byte
	webInputCh  <-chan []byte
	state       *gameState
	ticker      *time.Ticker    // serves as the game clock
	wgQuit      *sync.WaitGroup // wait group to make sure it quits safely
}

// Create a new game engine, casting channels to be uni-directional
func NewGameEngine(_webOutputCh chan<- []byte, _webInputCh <-chan []byte,
	_wgQuit *sync.WaitGroup, clockRate int32) *GameEngine {

	// Time between ticks
	_tickTime := 1000000 * time.Microsecond / time.Duration(clockRate)
	ge := GameEngine{
		quitCh:      make(chan struct{}),
		webOutputCh: _webOutputCh,
		webInputCh:  _webInputCh,
		state:       newGameState(),
		ticker:      time.NewTicker(_tickTime),
		wgQuit:      _wgQuit,
	}

	// Return the game engine
	return &ge
}

// Quit by closing the game engine, in case the loop ends
func (ge *GameEngine) quit() {

	// Log that the game engine successfully quit
	log.Println("\033[35mLOG:  Game engine successfully quit\033[0m")

	// Decrement the quit wait group counter
	ge.wgQuit.Done()
}

// Quit function exported to other packages
func (ge *GameEngine) Quit() {
	ge.quitCh <- struct{}{}
}

// Start the game engine - should be launched as a go-routine
func (ge *GameEngine) RunLoop() {

	// Quit if we ever run into an error or the program ends
	defer func() {
		ge.quit()
	}()

	// Increment the quit wait group counter
	ge.wgQuit.Add(1)

	// Update the number of active game engines
	// (Lock the mutex to prevent races in case of a multiple engine issue)
	var _activeGameEngines int
	muAGE.Lock()
	{
		activeGameEngines++
		_activeGameEngines = activeGameEngines
	}
	muAGE.Unlock()

	// If there was already a game engine, kill this one and throw an error
	if _activeGameEngines > 1 {
		log.Println("\033[35m\033[1mERR:  Cannot simultaneously dispatch more" +
			" than one game engine. Quitting...\033[0m")
		return
	}

	// Output buffer to store the serialized output
	outputBuf := make([]byte, 256)

	// Length of the serialized output
	serLen := 0

	// Flag to keep track of whether the last iteration of the loop was a tick
	justTicked := true

	for {

		/*
			If the game did not just tick, we know it was paused, so we can skip
			these steps as they were already done during the first paused tick
		*/
		if justTicked {

			/* STEP 1: Update the ghost positions if necessary */

			// If the game state is ready to update, update the ghost positions
			if ge.state.updateReady() {

				// Update all ghosts at once
				ge.state.updateAllGhosts()

				// Try to respawn Pacman (if it is at an empty location)
				ge.state.tryRespawnPacman()

				// If we should pause upon updating, do so
				if ge.state.getPauseOnUpdate() {
					ge.state.pause()
					ge.state.setPauseOnUpdate(false)
				}

				// Check for collisions
				ge.state.checkCollisions()

				/*
					Decrement all step counters, and decide if the mode, penalty,
					or fruit states should change
				*/
				ge.state.handleStepEvents()
			}

			/* STEP 2: Serialize the current game state to the output buffer */

			// Re-serialize the current state
			serLen = ge.state.serFull(outputBuf, 0)

			/* STEP 3: Start planning the next ghost moves if an update happened */

			// If we're ready for an update, plan the next ghost moves
			if ge.state.updateReady() {

				/*
					Acquire the ghost control lock, to prevent other actions like
					respawns/resets while updating the ghost state
				*/
				ge.state.planAllGhosts()
			}
		}

		/* STEP 4: Write the serialized game state to the output channel */

		// Check if a write will be blocked, and try to write the serialized state
		b := len(ge.webOutputCh) == cap(ge.webOutputCh)
		start := time.Now()
		ge.webOutputCh <- outputBuf[:serLen]

		/*
			If the write was blocked for too long (> 1ms), send a warning
			to the terminal
		*/
		if b {
			wait := time.Since(start)
			if wait > time.Millisecond {
				log.Printf("\033[35mWARN: The game engine output channel was "+
					"full (%s)\033[0m\n", wait)
			}
		}

		/* STEP 5: Read the input channel and update the game state accordingly */
		select {

		// If we get a message from the web broker, handle it
		case msg := <-ge.webInputCh:
			go ge.state.interpretCommand(msg)

		// If we get a quit signal, quit this broker
		case <-ge.quitCh:
			return

		/*
			If the web input channel hits full capacity, send a terminal warning

			What this means: either the clients are sending too much input,
			or the game loop can't keep up
		*/
		default:
			if len(ge.webInputCh) == cap(ge.webInputCh) {
				log.Println("\033[35mWARN: Game engine input channel full\033[0m")
			}
		}

		/* STEP 6: Update the game state for the next tick */

		// Increment the number of ticks
		if !ge.state.isPaused() {
			justTicked = true
			ge.state.nextTick()
		} else {
			justTicked = false
		}

		/* STEP 5: Wait for the ticker to complete the current frame */
		<-ge.ticker.C
	}
}
