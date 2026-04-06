Intelligent DDoS Detection and Mitigation in SDN 

🛡️📌 Project Overview

This project addresses the critical security challenges in Software-Defined Networks (SDNs), specifically focusing on the detection and mitigation of Distributed Denial of Service (DDoS) attacks. 
By decoupling the control plane from the data plane, SDNs offer flexibility but remain vulnerable to controller saturation.Our solution implements a Hybrid Machine Learning Framework that combines traditional classifiers with deep learning architectures to provide real-time, high-accuracy anomaly detection.

🚀 Key FeaturesHybrid Architecture: 

Integration of SVM, Random Forest, CNN-LSTM, and Transformer-RF models for robust classification.
Real-Time Detection: Processes live network traffic metadata to identify threats in milliseconds.
Automated Mitigation: Automatically triggers Flow-Mod entries via the SDN Controller to drop malicious traffic at the switch level.
Dual-Plane Analysis: Uses CNNs for spatial feature extraction and LSTMs/Transformers for temporal sequence analysis.
Interactive Dashboard: A web-based interface to monitor network health, traffic ratios, and model performance.

🏗️ System ArchitectureThe system follows a three-tier approach to network security:

Data Plane (Mininet): Generates and forwards network traffic using Open vSwitch (OVS).
Control Plane (Ryu/ONOS): Manages flow rules and communicates with the ML engine via Northbound APIs.
Application Plane (ML Engine): The "Brain" where traffic is preprocessed, classified, and mitigation decisions are made.
🛠️ Tech StackLanguage: Python 3.xSDN Tools: Mininet, OpenFlow 1.3ML 
Frameworks: TensorFlow, Keras, Scikit-learn, XGBoost 
Environment: Ubuntu 20.04/22.04 LTS
Documentation: Microsoft Office Suite (Project Report)

⚙️ Installation & Setup

Clone the Repository 

git clone https://github.com/your-username/sdn-ddos-hybrid-ml.git
cd sdn-ddos-hybrid-ml

Set up Virtual Environment

conda create -n sdn_env python=3.9
conda activate sdn_env
pip install -r requirements.txt

Initialize Mininet Topology

sudo mn --custom topology.py --topo mytopo --controller remote
Run the Detection Engine 
python app.py

📈 Performance MetricsThe system is evaluated based on the following:

Accuracy: Overall correctness of the model.
Precision/Recall: Efficiency in reducing False Positives (legitimate traffic being blocked).
Detection Latency: Time taken from attack start to Flow-Mod injection.

📝 KeywordsSDN • DDoS • Machine Learning • SVM • Random Forest • CNN-LSTM • Transformer-RF • Anomaly Detection • Cybersecurity • Network Security
