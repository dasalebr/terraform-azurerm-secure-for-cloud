# diagrams as code vía https://diagrams.mingrammer.com
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import ContainerInstances, ContainerRegistries, FunctionApps
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.analytics import EventHubs
from diagrams.azure.integration import EventGridDomains, AppConfiguration
from diagrams.azure.identity import EnterpriseApplications
from diagrams.custom import Custom

diagram_attr = {
    "pad": "0.25"
}

role_attr = {
    "imagescale": "false",
    "height": "1.5",
    "width": "3",
    "fontsize": "9",
}

with Diagram("Sysdig Secure for Cloud\n(Single Subscription)", graph_attr=diagram_attr, filename="diagram-tenant",
             show=True,
             direction="TB"):
    with Cluster("Azure Tenant"):
        with Cluster("Sysdig", graph_attr={"bgcolor": "lightblue"}):
            sds = Custom("Sysdig Secure", "../../resources/diag-sysdig-icon.png")

        with Cluster("Azure Account Subscription 2", graph_attr={"bgcolor": "seashell2"}):
            diagnosticSettings = AppConfiguration("Diagnostic Settings")
            with Cluster("Resource Group"):
                eventhubCC1 = EventHubs("Cloud Connector \n Event Hub")
                eventhubCS1 = EventHubs("Cloud Scanning \n Event Hub")
                cregistry = ContainerRegistries("ACR Task \n Image Scanning")

                diagnosticSettings >> eventhubCC1
                eventGrid = EventGridDomains("Event Grid")
                eventGrid << cregistry
                eventGrid >> eventhubCS1

        with Cluster("Azure Account Subscription 1 (workload)"):
            diagnosticSettings = AppConfiguration("Diagnostic Settings")
            with Cluster("Resource Group"):
                eventhubCC = EventHubs("Cloud Connector \n Event Hub")
                eventhubCS = EventHubs("Cloud Scanning \n Event Hub")
                diagnosticSettings >> eventhubCC
                with Cluster("Container Instance Group"):
                    cc = ContainerInstances("Cloud Connector \n Container Instance")
                ccConfig = StorageAccounts("Cloud Connector \n config")

                app = EnterpriseApplications("Enterprise App")
                cregistry = ContainerRegistries("ACR Task \n Image Scanning")
                eventGrid = EventGridDomains("Event Grid")
                bench = Custom("Azure Lighthouse \n CSPM", "../../resources/diag-lighthouse.jpeg")

                ccConfig >> Edge(style="dashed", label="Get CC \n config file") >> cc
                cregistry << app

                eventhubCC >> cc
                eventhubCS >> cc
                cc >> app

                eventGrid << cregistry
                eventGrid >> eventhubCS

                sds << Edge(style="dashed") << cc
                bench >> sds

                eventhubCC1 >> cc
                eventhubCS1 >> cc