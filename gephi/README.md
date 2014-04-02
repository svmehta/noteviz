Driver for layout and modularity calculation which utilizes gephi toolkit

To build fat jar execute:
mvn clean compile assembly:single

To layout the graph using the ForceAtlas2 algorithm and color nodes according to communities output from modularity algorithm run:
java -jar target/LayoutPlugin-1.0-jar-with-dependencies.jar <inputFilePath> <outputFilePath>