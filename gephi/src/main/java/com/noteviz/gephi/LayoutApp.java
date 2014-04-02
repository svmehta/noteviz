package com.noteviz.gephi;

import java.io.File;
import java.io.IOException;

import org.gephi.data.attributes.api.AttributeColumn;
import org.gephi.data.attributes.api.AttributeController;
import org.gephi.data.attributes.api.AttributeModel;
import org.gephi.filters.api.FilterController;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.UndirectedGraph;
import org.gephi.statistics.plugin.Modularity;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.EdgeDefault;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2;
import org.gephi.layout.spi.LayoutProperty;
import org.gephi.partition.api.Partition;
import org.gephi.partition.api.PartitionController;
import org.gephi.partition.plugin.NodeColorTransformer;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.ranking.api.RankingController;
import org.openide.util.Lookup;

public class LayoutApp {

    private String importFilePath;
    private String exportFilePath;

    public LayoutApp (String importFilePath, String exportFilePath) {
        this.importFilePath = importFilePath;
        this.exportFilePath = exportFilePath;
    }

    public void run() {
        System.out.println("Run LayoutApp on " + importFilePath);
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();

        //Get models and controllers for this new workspace - will be useful later
        AttributeModel attributeModel = Lookup.getDefault().lookup(AttributeController.class).getModel();
        GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getModel();
        PreviewModel model = Lookup.getDefault().lookup(PreviewController.class).getModel();
        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        FilterController filterController = Lookup.getDefault().lookup(FilterController.class);
        RankingController rankingController = Lookup.getDefault().lookup(RankingController.class);

        // load gexf file
        Container container;
        try {
            File file = new File(this.importFilePath);
            container = importController.importFile(file);
            container.getLoader().setEdgeDefault(EdgeDefault.UNDIRECTED);   //Force UNDIRECTED
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }

        //Append imported data to GraphAPI
        importController.process(container, new DefaultProcessor(), workspace);

        //See if graph is well imported
        UndirectedGraph graph = graphModel.getUndirectedGraph();
        System.out.println("Nodes: " + graph.getNodeCount());
        System.out.println("Edges: " + graph.getEdgeCount());

        //Run modularity algorithm - community detection
        Modularity modularity = new Modularity();
        modularity.execute(graphModel, attributeModel);

        //Partition with 'modularity_class', just created by Modularity algorithm
        System.out.println("Running modularity calculation");
        PartitionController partitionController = Lookup.getDefault().lookup(PartitionController.class);
        AttributeColumn modColumn = attributeModel.getNodeTable().getColumn(Modularity.MODULARITY_CLASS);
        Partition p = partitionController.buildPartition(modColumn, graph);
        System.out.println(p.getPartsCount() + " partitions found");
        NodeColorTransformer nodeColorTransformer = new NodeColorTransformer();
        nodeColorTransformer.randomizeColors(p);
        partitionController.transform(p, nodeColorTransformer);
        

        //Run ForceAtlas2 layout for 2000 iterations
        System.out.println("Starting layout ForceAtlas2");
        ForceAtlas2 forceLayout = new ForceAtlas2(null);
        forceLayout.setGraphModel(graphModel);
        forceLayout.resetPropertiesValues();
        forceLayout.setJitterTolerance(0.3);
        forceLayout.initAlgo();
        for (int i = 0; i < 2000 && forceLayout.canAlgo(); i++) {
        	forceLayout.goAlgo();
        	if (i%100 == 0) {
            	System.out.println("force layout step: " + i);
        	}
        }
        forceLayout.endAlgo();
        System.out.println("End layout");

        //Export full graph
        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        try {
            ec.exportFile(new File(this.exportFilePath));
            System.out.println("export complete");
        } catch (IOException ex) {
            ex.printStackTrace();
            return;
        }

    }
}