"""
Kitchen Timer Service
Manages multiple simultaneous timers with real-time WebSocket updates
"""
import threading
import time
from datetime import datetime


class TimerService:
    """Service for managing kitchen timers"""
    
    def __init__(self):
        self.active_timers = {}  # {timer_id: {'thread': thread, 'stop_event': event}}
        self.lock = threading.Lock()
    
    def start_timer(self, timer_id, duration, socketio):
        """Start a new timer with WebSocket updates"""
        
        with self.lock:
            # Don't start if already running
            if timer_id in self.active_timers:
                return False
            
            # Create stop event for this timer
            stop_event = threading.Event()
            
            # Create and start timer thread
            timer_thread = threading.Thread(
                target=self._timer_worker,
                args=(timer_id, duration, stop_event, socketio),
                daemon=True
            )
            
            self.active_timers[timer_id] = {
                'thread': timer_thread,
                'stop_event': stop_event,
                'duration': duration,
                'started_at': datetime.utcnow()
            }
            
            timer_thread.start()
            
            return True
    
    def stop_timer(self, timer_id):
        """Stop a running timer"""
        
        with self.lock:
            if timer_id not in self.active_timers:
                return False
            
            # Signal the timer to stop
            self.active_timers[timer_id]['stop_event'].set()
            
            # Remove from active timers
            del self.active_timers[timer_id]
            
            return True
    
    def get_active_timers(self):
        """Get list of active timer IDs"""
        with self.lock:
            return list(self.active_timers.keys())
    
    def _timer_worker(self, timer_id, duration, stop_event, socketio):
        """Worker thread for a single timer"""
        
        start_time = time.time()
        
        while not stop_event.is_set():
            # Calculate elapsed and remaining time
            elapsed = int(time.time() - start_time)
            remaining = max(0, duration - elapsed)
            
            # Check if timer is complete
            if remaining <= 0:
                # Emit completion event
                try:
                    socketio.emit('timer_complete', {
                        'timer_id': timer_id,
                        'duration': duration,
                        'completed_at': datetime.utcnow().isoformat()
                    })
                except Exception as e:
                    print(f"Error emitting timer_complete: {e}")
                
                # Remove from active timers
                with self.lock:
                    if timer_id in self.active_timers:
                        del self.active_timers[timer_id]
                
                break
            
            # Emit update every second
            try:
                socketio.emit('timer_update', {
                    'timer_id': timer_id,
                    'elapsed': elapsed,
                    'remaining': remaining,
                    'duration': duration,
                    'timestamp': datetime.utcnow().isoformat()
                })
            except Exception as e:
                print(f"Error emitting timer_update: {e}")
            
            # Sleep for 1 second (or until stop event)
            stop_event.wait(1)
    
    def stop_all_timers(self):
        """Stop all active timers"""
        
        with self.lock:
            timer_ids = list(self.active_timers.keys())
        
        for timer_id in timer_ids:
            self.stop_timer(timer_id)
