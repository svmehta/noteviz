Requirements
python
java

TO INSTALL DEPENDENCIES
pip install -r requirements.txt


The short version:
Input: a path to your evernote files in html format
Output: a network visualization of your notes over time based on auto-generated tags

The long version:

Export your evernote notes to a folder using the desktop client - I exported

python run.py <path to directory of note html>

This will autogenerate tags for each of your notes (by sending the bag of words representing your note to the wikipedia miner toolkit in plaintext! Only use with non-sensitive data), compute pairwise similarity between each set of notes, and output a graph in .gexf format based on these nodes and edges.

This will generate a .gexf file which can be laid out using the gephi toolkit plugin


To layout the graph

Driver for layout and modularity calculation which utilizes gephi toolkit

To build fat jar execute:
mvn clean compile assembly:single

To layout the graph using the ForceAtlas2 algorithm and color nodes according to communities output from modularity algorithm run:
java -jar target/LayoutPlugin-1.0-jar-with-dependencies.jar <inputFilePath> <outputFilePath>