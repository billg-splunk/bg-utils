## Debug traces using the Smart Agent
* Install ngrep
  * ```sudo apt-get install ngrep```
* Run the command to monitor the SA port looking for traces
  * ```sudo ngrep -d lo port 9080```