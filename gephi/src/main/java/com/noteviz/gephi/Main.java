package com.noteviz.gephi;

public class Main {
    public static void main( String[] args ) {
    	for (int i = 0; i<args.length; i++) {
    		System.out.println(args[i]);
    	}
    	
    	if(args.length < 2) {
    		System.out.println("Must specify input and output filename as command line arguments");
    		System.out.println("Usage: java -jar target/LayoutPlugin-1.0-jar-with-dependencies.jar <inputFilePath> <outputFilePath>");
    		System.exit(0);
    	}

    	System.out.println( "Running layout generator");    	
		LayoutApp layoutApp = new LayoutApp(args[0], args[1]);
		layoutApp.run();

    }
}
