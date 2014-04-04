# The short version:
+ Input: a path to your evernote files in html format
+ Output: a network visualization of your notes over time based on auto-generated tags
+ demo: http://evernoteviz.com

# The long version:

### Requirements
+ python 2.x
+ java
+ maven

### Install Dependencies
+ pip install -r requirements.txt

### Export
+ Export as HTML all of your evernote notes to a folder using the desktop client

### Generate Tags and Graph

python run.py &lt;path to directory of notes&gt;

This will...
+ Autogenerate tags for each of your notes (by sending the bag of words representing your note to the wikipedia miner toolkit in plaintext! Only use with non-sensitive data)
+ Computes pairwise similarity between each set of notes according to their tags
+ Outputs a graph in .gexf format based on these nodes and edges.

### Layout Graph with Gephi Toolkit
+ Driver for layout and modularity calculation which utilizes gephi toolkit

To build fat jar execute:
+ mvn clean compile assembly:single

To layout the graph using the ForceAtlas2 algorithm and color nodes according to communities output from modularity algorithm run:
+ java -jar target/LayoutPlugin-1.0-jar-with-dependencies.jar &lt;inputFilePath&gt; &lt;outputFilePath&gt;

### Visualize graph with Sigma.js
+ Copy network.gexf and accTags.json files to the public subfolder of web and load index.html in a (modern) web browser
