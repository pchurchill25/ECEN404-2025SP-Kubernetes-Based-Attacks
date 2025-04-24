# GUI Attack Framework
This is a general overview of how to implement an attack in the GUI.

## Adding the attack
```
def runattack(self):
        command = f"<insert command to run attack here>"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) #this runs your attack in a background process so it doesn't freeze the GUI.
        stdout, stderr = process.communicate()
```
## Adding the buttons
```
  self.startButton = QPushButton("Start Attack", clicked=self.runattack) #ties your attack function to a button
  attackButtonLayout.addWidget(self.startButton) #adds your button to the row of attacks
```
