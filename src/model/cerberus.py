from model.bot import Bot, BotStatus
import time


class Cerberus(Bot):
    def __init__(self):
        super().__init__()
        self.iterations = 10

    def main_loop(self):
        '''
        Main bot loop. This function should be called on another thread. It will run according to the bot's status.
        This loop is protected by a timeout so that the bot will stop if it takes too long, preventing leaks.
        '''
        while self.current_iter < self.iterations and self.status != BotStatus.STOPPED:
            pause_limit = 10  # TODO: 10 second pause limit, remove later
            self.increment_iter()
            print(f"main_loop() from cerberus.py - iteration: {self.current_iter} out of {self.iterations}")
            # if status is stopped, break and print message
            if self.status == BotStatus.STOPPED:
                print("main_loop() from cerberus.py - bot is stopped, breaking...")
                break
            # if status is paused, sleep for one second and continue until timeout
            while self.status == BotStatus.PAUSED:
                print("main_loop() from cerberus.py - bot is paused, sleeping...")
                time.sleep(1)
                # if bot is stopped, break
                if self.status == BotStatus.STOPPED:
                    print("main_loop() from cerberus.py - bot is stopped, breaking from pause...")
                    break
                pause_limit -= 1
                if pause_limit == 0:
                    print("main_loop() from cerberus.py - bot is paused, timeout reached, stopping...")
                    self.stop()
                    break
            time.sleep(1)
        print("main_loop() from cerberus.py - bot has terminated or reached the end of its iterations")
        # if bot hasn't been stopped yet...
        if self.status != BotStatus.STOPPED:
            self.set_status(BotStatus.STOPPED)
            self.reset_iter()