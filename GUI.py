import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import subprocess
import threading
import time
import csv
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt



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
        self.setGeometry(200, 200, 1200, 225)  # Set window size

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

        self.recording_enabled = False
        self.csv_filename = "top_nodes_log.csv"

        self.recordButton = QPushButton("Start Recording", self)
        self.recordButton.clicked.connect(self.toggle_recording)
        layout.addWidget(self.recordButton)

    def toggle_recording(self):
        if not self.recording_enabled:
            # Ask user to choose file path
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV File",
                "top_nodes_log.csv",
                "CSV Files (*.csv);;All Files (*)",
                options=options
            )
            if filename:
                self.csv_filename = filename
                self.recording_enabled = True
                self.recordButton.setText("Stop Recording")

                # Write CSV headers
                with open(self.csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Node", "CPU(cores)", "Memory(bytes)"])
            else:
                # User canceled
                return
        else:
            self.recording_enabled = False
            self.recordButton.setText("Start Recording")

    def run_top_nodes(self):
        self.executor = CommandExecutor("kubectl top nodes")
        self.executor.command_output_signal.connect(self.update_output)
        self.executor.start()

    def update_output(self, output):
        self.outputDisplay.setPlainText(output)

        if self.recording_enabled:
            lines = output.strip().split('\n')
            if len(lines) > 1:
                headers = lines[0].split()
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            node, cpu, mem = parts[0], parts[1], parts[2]
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            with open(self.csv_filename, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([timestamp, node, cpu, mem])


class NodeAttackToggle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toggle Node Attack")
        self.resize(400, 300)

        self.toggle_state = False  # False = not running

        self.toggle_button = QPushButton("Start Attack")
        self.toggle_button.clicked.connect(self.toggle_attack)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.output_box)
        self.setLayout(layout)

    def toggle_attack(self):
        if not self.toggle_state:
            # Start attack
            command = "kubectl apply -f api-dos-deployment.yaml"
            self.toggle_button.setText("Stop Attack")
        else:
            # Stop attack
            command = "kubectl delete -f api-dos-deployment.yaml"
            self.toggle_button.setText("Start Attack")

        self.toggle_state = not self.toggle_state

        self.executor = CommandExecutor(command)
        self.executor.command_output_signal.connect(self.display_output)
        self.executor.start()

    def display_output(self, output):
        self.output_box.append(output)

class ContainerCountWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Active Container Count")
        self.setGeometry(300, 300, 300, 100)  # Window position and size

        layout = QVBoxLayout()
        self.containerCountLabel = QLabel("Active Containers: 0")
        layout.addWidget(self.containerCountLabel)
        self.setLayout(layout)

        # Timer to update the container count every second
        self.containerTimer = QTimer(self)
        self.containerTimer.timeout.connect(self.updateContainerCount)
        self.containerTimer.start(1000)  # Update every second

    def updateContainerCount(self):
        try:
            result = subprocess.run("docker ps -q --filter 'ancestor=spam_container_image' | wc -l",
                                    shell=True, capture_output=True, text=True)
            count = result.stdout.strip()
            self.containerCountLabel.setText(f"Active Containers: {count}")
        except Exception as e:
            self.containerCountLabel.setText("Error Fetching Count")

    def closeEvent(self, event):
        """ Stop the timer when the window is closed """
        self.containerTimer.stop()
        event.accept()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_attack_running = False
        self.image_container_id = None
        self.pod_process = None
        self.window_width, self.window_height = 3000, 1500
        self.setMinimumSize(self.window_width, self.window_height)

        # Pod Attack
        self.containerWindow = None  # Track the separate container window
        self.window_width, self.window_height = 1200, 1500
        self.setMinimumSize(self.window_width, self.window_height)
        self.pod_attack_running = False  # for pod attack only

        #self.setWindowTitle('GUI test')



        # Top-level vertical layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # First row: Attack Buttons
        layout.label = QLabel("Enter Filename (without .pcap):")
        attackLabel = QLabel("Attack Controls")
        attackLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(attackLabel)

        attackButtonLayout = QHBoxLayout()
        attackRow = QHBoxLayout()
        attackRow.addStretch()
        attackRow.addLayout(attackButtonLayout)
        attackRow.addStretch()
        layout.addLayout(attackRow)

        # Second row: Data Collection Controls
        self.label = QLabel("Enter Filename (without .pcap):")

        dataLabel = QLabel("Data Collection")
        dataLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(dataLabel)

        dataLayout = QHBoxLayout()
        dataRow = QHBoxLayout()
        dataRow.addStretch()
        dataRow.addLayout(dataLayout)
        dataRow.addStretch()
        layout.addLayout(dataRow)

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
        dataLayout.addWidget(self.button_run)
#tcpdump run button
        self.startButton = QPushButton("Start TCPDump", clicked=self.start_tcpdump)
        dataLayout.addWidget(self.startButton)
#tcpdump stop button
        self.stopButton = QPushButton("Stop TCPDump", clicked=self.stop_tcpdump)
        dataLayout.addWidget(self.stopButton)
#image attack run button:
        self.imageToggleButton = QPushButton("Run Image Attack", clicked=self.toggle_image_attack)
        attackButtonLayout.addWidget(self.imageToggleButton)

        #self.imageButton = QPushButton("Run Image Attack", clicked=self.runimage)
       # attackButtonLayout.addWidget(self.imageButton)

        #self.imageStopButton = QPushButton("Stop Image Attack", clicked=self.stopimage)
        #attackButtonLayout.addWidget(self.imageStopButton)
        self.nodeToggleButton = QPushButton("Start Node Attack", clicked=self.toggle_node_attack)
        attackButtonLayout.addWidget(self.nodeToggleButton)

        self.node_attack_running = False

        # pod attack run/stop toggle button:
        self.podToggleButton = QPushButton("Run Pod Attack", clicked=self.toggle_pod_attack)
        attackButtonLayout.addWidget(self.podToggleButton)

        self.podDeleteButton = QPushButton("Delete Pod Attack", clicked=self.deletePod)
        attackButtonLayout.addWidget(self.podDeleteButton)

        # Button to open "kubectl top nodes" window
        self.kubectlTopButton = QPushButton("Show Kubectl Top Nodes", clicked=self.show_kubectl_top_nodes)
        dataLayout.addWidget(self.kubectlTopButton)

        # self.editorCommand.insertPlainText('dir')
    def toggle_node_attack(self):
        if not self.node_attack_running:
            command = "kubectl apply -f api-dos-deployment.yaml"
            self.nodeToggleButton.setText("Stop Node Attack")
        else:
            command = "kubectl delete -f api-dos-deployment.yaml"
            self.nodeToggleButton.setText("Start Node Attack")

        self.node_attack_running = not self.node_attack_running

        self.executor = CommandExecutor(command)
        self.executor.command_output_signal.connect(self.update_output)
        self.executor.start()
    # toggle function for image attack button
    def toggle_image_attack(self):
        if not self.image_attack_running:
            self.runimage()
            self.imageToggleButton.setText("Stop Image Attack")
            self.image_attack_running = True
        else:
            self.stopimage()
            self.imageToggleButton.setText("Run Image Attack")
            self.image_attack_running = False

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
        self.editorOutput.insertPlainText(f"Trying to run: fakeimage\n")

        command = f"docker run fakeimage"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            self.editorOutput.insertPlainText(f"Error encountered: {stderr}\n")
            self.editorOutput.insertPlainText("Falling back to 'hw' image in detached mode...\n")

            # Run fallback image in detached mode
            fallback_command = "docker run -d hw"
            process = subprocess.Popen(fallback_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.image_container_id = stdout.strip()
                self.editorOutput.insertPlainText(f"'hw' container started: {self.image_container_id}\n")
            else:
                self.editorOutput.insertPlainText(f"Failed to start fallback container: {stderr}\n")
        else:
            self.editorOutput.insertPlainText("Real image called\n")


    def stopimage(self):
        if self.image_container_id:
            stop_command = f"docker stop {self.image_container_id}"
            process = subprocess.Popen(stop_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.editorOutput.insertPlainText(f"Stopped container: {self.image_container_id}\n")
                self.image_container_id = None
            else:
                self.editorOutput.insertPlainText(f"Failed to stop container: {stderr}\n")
        else:
            self.editorOutput.insertPlainText("No image attack is currently running.\n")


    def runNode(self):

            command_imge = "kubectl apply -f api-dos-deployment.yaml"  # ).toPlainText().strip()
            txt = os.popen(command_imge)
            #self.editorPodStatus.clear()
            #self.track_pods_live()
            if txt:
                self.editorOutput.clear()
                output = txt.read()
                self.editorOutput.insertPlainText(output)

    def deleteNode(self):

        command_imge = "kubectl delete -f api-dos-deployment.yaml"  # ).toPlainText().strip()
        txt = os.popen(command_imge)
        self.pod_tracking_active = False
        if txt:
            self.editorOutput.clear()
            output = txt.read()
            self.editorOutput.insertPlainText(output)

    # toggle function for image attack button
    def toggle_pod_attack(self):
        if not self.pod_attack_running:
            self.runPod()
            self.podToggleButton.setText("Stop Pod Attack")
            self.pod_attack_running = True
        else:
            self.stopPod()
            self.podToggleButton.setText("Run Pod Attack")
            self.pod_attack_running = False

    def runPod(self):
        if self.pod_process is None:
            self.pod_process = subprocess.Popen(["bash", "cont_flood.sh"], stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE, text=True)

            self.editorOutput.insertPlainText("Pod attack started...\n")
            # self.containerTimer.start(1000)
            if self.containerWindow is None:
                self.containerWindow = ContainerCountWindow()
            self.containerWindow.show()

        else:
            self.editorOutput.insertPlainText("Pod attack is already running!\n")

    def stopPod(self):
        if self.pod_process is not None:
            self.pod_process.terminate()  # Try to terminate gracefully
            try:
                self.pod_process.wait(timeout=5)  # Give it time to exit
            except subprocess.TimeoutExpired:
                self.pod_process.kill()  # Force kill if necessary

            self.pod_process = None  # Reset reference
            self.editorOutput.insertPlainText("Pod attack script stopped.\n")

            # Close the container count window
            if self.containerWindow:
                self.containerWindow.close()
                self.containerWindow = None

            # Kill all background CPU-consuming processes more aggressively
            subprocess.run("pkill -9 -f 'echo.*13**99'", shell=True)  # Ensure all CPU-consuming loops are killed
            subprocess.run("pkill -9 -f 'bash cont_flood.sh'", shell=True)  # Ensure the script itself is killed

        else:
            self.editorOutput.insertPlainText("No Pod attack is running.\n")

    def deletePod(self):
        # Stop all running spam containers
        subprocess.run("docker stop $(docker ps -q --filter 'ancestor=spam_container_image')", shell=True)
        subprocess.run("docker rm $(docker ps -a -q --filter 'ancestor=spam_container_image')", shell=True)
        # Force kill any remaining CPU-consuming processes
        subprocess.run("pkill -9 -f 'echo.*13**99'", shell=True)
        subprocess.run("pkill -9 -f 'bash cont_flood.sh'", shell=True)
        # Remove the attack image to prevent further execution
        subprocess.run("docker rmi -f spam_container_image", shell=True)

        # Close the container count window
        if self.containerWindow:
            self.containerWindow.close()
            self.containerWindow = None

        self.editorOutput.insertPlainText("Pod attack containers, processes, and image deleted.\n")


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    courier_font = QFont("Courier", 10)
    app.setFont(courier_font)
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

