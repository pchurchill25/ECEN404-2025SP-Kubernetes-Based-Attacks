import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QTimer




#trying to execute the TCP dump
class CommandExecutor(QThread):
    command_output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            output = os.popen(self.command).read()
            self.command_output_signal.emit(output)
        except Exception as e:
            self.command_output_signal.emit(f"Error: {e}")


class KubectlTopNodesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kubectl Top Nodes Output")
        self.setGeometry(200, 200, 1000, 170)  # Set window size

        layout = QVBoxLayout()
        self.outputDisplay = QPlainTextEdit()
        self.outputDisplay.setReadOnly(True)
        layout.addWidget(self.outputDisplay)

        self.setLayout(layout)

        # Timer for auto-refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_top_nodes)
        self.timer.start(1000)  # Refresh every second

        # Run first update immediately
        self.run_top_nodes()

    def run_top_nodes(self):
        self.executor = CommandExecutor("kubectl top nodes")
        self.executor.command_output_signal.connect(self.update_output)
        self.executor.start()

    def update_output(self, output):
        self.outputDisplay.setPlainText(output)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 1500
        self.setMinimumSize(self.window_width, self.window_height)

        self.setWindowTitle('GUI test')
        layout = QVBoxLayout()
        self.setLayout(layout)

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        self.label = QLabel("Enter Filename (without .pcap):")
        layout.addWidget(self.label)

        self.filenameInput = QLineEdit()
        layout.addWidget(self.filenameInput)

        self.label = QLabel("Enter Terminal Command:")
        layout.addWidget(self.label)

        self.editorCommand = QPlainTextEdit()
        layout.addWidget(self.editorCommand)


    #area to type in filename

    #set filename

        self.label = QLabel("Terminal Output:")
        layout.addWidget(self.label)

        self.editorOutput = QPlainTextEdit()
        layout.addWidget(self.editorOutput, 7)

        self.button_run = QPushButton('&run', clicked=self.runcommand)
        buttonLayout.addWidget(self.button_run)
#tcpdump run button
        self.startButton = QPushButton("Start TCPDump", clicked=self.start_tcpdump)
        buttonLayout.addWidget(self.startButton)
#tcpdump stop button
        self.stopButton = QPushButton("Stop TCPDump", clicked=self.stop_tcpdump)
        buttonLayout.addWidget(self.stopButton)
#image attack run button:
        self.imageButton = QPushButton("Run Image Attack",clicked = self.runimage)
        buttonLayout.addWidget(self.imageButton)

# node attack RUN button
        self.nodeRunButton = QPushButton("Run Node Attack", clicked=self.runNode)
        buttonLayout.addWidget(self.nodeRunButton)

# node attack DELETE button
        self.nodeDeleteButton = QPushButton("Delete Node Attack", clicked=self.deleteNode)
        buttonLayout.addWidget(self.nodeDeleteButton)

    # image attack run button:
        self.podButton = QPushButton("Run Pod Attack", clicked=self.runPod)
        buttonLayout.addWidget(self.podButton)

        # Button to open "kubectl top nodes" window
        self.kubectlTopButton = QPushButton("Show Kubectl Top Nodes", clicked=self.show_kubectl_top_nodes)
        buttonLayout.addWidget(self.kubectlTopButton)

        # self.button_clear = QPushButton('&Clear', clicked=lambda: self.editorOutput.clear())
        # buttonLayout.addWidget(self.button_clear)

        # self.editorCommand.insertPlainText('dir')

    def show_kubectl_top_nodes(self):
        self.kubectlWindow = KubectlTopNodesWindow()
        self.kubectlWindow.show()





#TCP dump function
    def start_tcpdump(self):
        filename = self.filenameInput.text().strip()
        if not filename:
            self.editorOutput.insertPlainText("Error: Please enter a valid filename.\n")
            return

        full_command = (
            f"kubectl exec -it tcpdump-pod -- sh -c 'tcpdump -i any -w /tmp/{filename}.pcap'"
        )

        self.execute_command_in_background(full_command)

    def execute_command_in_background(self, command):
        self.executor = CommandExecutor(command)
        self.executor.command_output_signal.connect(self.update_output)
        self.executor.start()

    def stop_tcpdump(self):
        stop_command = "kubectl exec -it tcpdump-pod -- pkill -f tcpdump"
        self.execute_command_in_background(stop_command)

        # Add a short delay to ensure tcpdump stops before copying the file
        self.executor.finished.connect(self.copy_pcap_file)

    def copy_pcap_file(self):
        filename = self.filenameInput.text().strip()
        if not filename:
            self.editorOutput.insertPlainText("Error: No filename provided.\n")
            return

        copy_command = f"kubectl cp tcpdump-pod:/tmp/{filename}.pcap /home/child3/Downloads/{filename}.pcap"
        self.execute_command_in_background(copy_command)

    def update_output(self, output):
        self.editorOutput.insertPlainText(output + "\n")



    def runcommand(self):
        command_line = self.editorCommand.toPlainText().strip()
        p = os.popen(command_line)
        if p:
            self.editorOutput.clear()
            output = p.read()
            self.editorOutput.insertPlainText(output)



#image attack run function
    def runimage(self):
        #self.window = KTN()
        #self.window.show()
        #command_imge = "gnome-terminal"  # ).toPlainText().strip()
        #txt = os.popen(command_imge)
        #if txt:
        #    self.editorOutput.clear()
        #    output = txt.read()
        #    self.editorOutput.insertPlainText(output)

        #command_imge = "sudo -s"  # ).toPlainText().strip()
        #txt = os.popen(command_imge)
        #if txt:
        #    self.editorOutput.clear()
        #    output = txt.read()
        #    self.editorOutput.insertPlainText(output)


        command_imge = "docker run hw" #).toPlainText().strip()
        self.executor = CommandExecutor(command_imge)
        self.executor.command_output_signal.connect(self.update_output)
        self.executor.start()
        #open window to display attack results in

            #attack starts here, will freeze current window while running, so open another window and display kubectl top nodes in it

    def runNode(self):

        command_imge = "kubectl apply -f api-dos-deployment.yaml"  # ).toPlainText().strip()
        txt = os.popen(command_imge)
        if txt:
            self.editorOutput.clear()
            output = txt.read()
            self.editorOutput.insertPlainText(output)

    def deleteNode(self):

        command_imge = "kubectl delete -f api-dos-deployment.yaml"  # ).toPlainText().strip()
        txt = os.popen(command_imge)
        if txt:
            self.editorOutput.clear()
            output = txt.read()
            self.editorOutput.insertPlainText(output)

    def runPod(self):

        command_imge = "bash image_flood.sh"    # ).toPlainText().strip()
        txt = os.popen(command_imge)
        if txt:
            self.editorOutput.clear()
            output = txt.read()
            self.editorOutput.insertPlainText(output)

    def stopPod(self):

        # command_imge = "bash image_flood.sh"    # ).toPlainText().strip()
        txt = os.popen(command_imge)
        if txt:
            self.editorOutput.clear()
            output = txt.read()
            self.editorOutput.insertPlainText(output)

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

