# Observations

### Temperature
Through changing up the temperature values, I was able to find out how the "mood" of the output changed. In some cases, it went on a bit more chaotic side while in some, it just displayed the bare minimum. Through experimenting with the values I was able to find out that the sweet spot for a standard assistant was ```0.7```. Additionally, I experimented with it a bit more and decided on giving the program 3 different moods that would make the interaction a bit more fun. I settled on ```a Pirate```, ```a Comedian``` and ```a Sports Commentator```. 

All of these required me to give them different temperatures in addition to specified styles that made them sound more like the role. The temperature for each of them was ```0.9``` for the Pirate, ```1.1``` for the Comedian and ```0.8``` for the Sports Commentator. Increasing the temperature more just made the outputs not make sense in some cases but with these, i was able to have a much more consistent output for each of the mood.

### Max Tokens
Additionally, by defining how many tokens the output should be, i thought of adding an option where the user can set a length for the output. I added in the option for ```Short```, ```Medium``` and ```Detailed``` length of the summary. For this, I didn't specifically need to set a number as it just generated a summary according to the option.