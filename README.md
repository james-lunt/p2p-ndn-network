# p2p name-defined-network
Group project for TCD module CS7NS1: Scalable Computing. We create a peer-to-peer name defined network which is built to communicate on multiple Raspberry Pi's. We use an underwater mission as an example emulation.

Group 18 NDN run instructions.
The following instructions is to run our two name defined networks on independent Raspberry Pi’s.
First, clone the following repo onto each raspberry Pi or download and transfer the codebase attacked. james-lunt/peer-to-peer-name-defined-network:

On Pi 1 Cd into the project folder.\newline
Run the command:  source .tmux/ndn-divers
This starts the diver network.
On Pi 2 Cd into the project folder.
Run the command: source .tmux/ndn-scientists
The follow can be done on either or both Pi’s
Run the command: tmux attach
This allows you to interface with the nodes in the network.
To see a list of selectable node press ctrl+b then w.
Select a node with the arrow keys and press enter to use the nodes terminal.
The nodes command lines prompts to ‘Ask the network for information:’. Type in some data name from this list of data names at the end of this document. If an invalid name is typed the data won’t send.
Wait for the data to return. You can track the routing by switching to other nodes.
To exit tmux, press ctrl+b then d.
To kill the network and all running ports, enter the command: tmux kill-server
