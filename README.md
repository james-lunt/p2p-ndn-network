# p2p name-defined-network
Group project for TCD module CS7NS1: Scalable Computing. We create a peer-to-peer name defined network which is built to communicate on multiple Raspberry Pi's. We use an underwater mission as an example emulation.

Group 18 NDN run instructions.
The following instructions is to run our two name defined networks on independent Raspberry Pi’s.

On Pi 1 Cd into the project folder.\newline
Run the command:  source .tmux/ndn-divers \newline
This starts the diver network.\newline
On Pi 2 Cd into the project folder. \newline
Run the command: source .tmux/ndn-scientists\newline
The follow can be done on either or both Pi’s\newline
Run the command: tmux attach\newline
This allows you to interface with the nodes in the network.\newline
To see a list of selectable node press ctrl+b then w.\newline
Select a node with the arrow keys and press enter to use the nodes terminal.\newline
The nodes command lines prompts to ‘Ask the network for information:’. Type in some data name from this list of data names at the end of this document. If an invalid name is typed the data won’t send.\newline
Wait for the data to return. You can track the routing by switching to other nodes.\newline
To exit tmux, press ctrl+b then d.\newline
To kill the network and all running ports, enter the command: tmux kill-server
