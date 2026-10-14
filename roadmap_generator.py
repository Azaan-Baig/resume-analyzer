LEARNING_RESOURCES = {
    "Python": "Learn Python fundamentals, functions, modules and OOP.",
    "SQL": "Learn SELECT, WHERE, JOIN, GROUP BY, subqueries and aggregation.",
    "Excel": "Learn formulas, pivot tables, charts and data analysis.",
    "Pandas": "Learn DataFrames, filtering, grouping, merging and data cleaning.",
    "Power BI": "Learn Power Query, data modeling, DAX and dashboards.",
    "Machine Learning": "Learn regression, classification, preprocessing and evaluation.",
    "scikit-learn": "Practice preprocessing, pipelines, model training and evaluation.",
    "FastAPI": "Learn how to build REST APIs and serve ML models with FastAPI.",
    "Docker": "Learn images, containers, Dockerfiles and basic deployment.",
    "MLflow": "Learn experiment tracking, model logging and model management.",
    "Deep Learning": "Learn neural networks, backpropagation and deep-learning workflows.",
    "LLM": "Learn LLM fundamentals, prompting and model integration.",
    "RAG": "Learn embeddings, retrieval, vector databases and RAG pipelines.",
    "NLP": "Learn tokenization, embeddings, text classification and NLP workflows.",
    "Transformers": "Learn Transformer architecture and Hugging Face workflows.",
    "Hugging Face": "Learn pretrained models, tokenizers and the Transformers library.",
    "OpenCV": "Learn image processing, contours, video and computer-vision basics.",
    "CNN": "Learn convolution, pooling and image classification with CNNs.",
    "YOLO": "Learn object detection, bounding boxes and YOLO workflows.",
    "PyTorch": "Learn tensors, datasets, neural networks and model training.",
    "TensorFlow": "Learn tensors, neural networks and model training with TensorFlow.",
    "Git": "Learn commits, branches, merges and version control.",
    "GitHub": "Learn repositories, branches, pull requests and collaboration.",
    "AWS": "Learn cloud fundamentals and deploying applications on AWS.",
    "Azure": "Learn Azure cloud fundamentals and deployment.",
    "GCP": "Learn Google Cloud fundamentals and deployment.",
    "APIs": "Learn REST APIs, HTTP methods, JSON and API integration.",
    "NumPy": "Learn arrays, vectorization and numerical computing.",
    "Matplotlib": "Learn charts, figures and basic data visualization.",
    "PostgreSQL": "Learn relational database design, SQL and PostgreSQL.",
    "MySQL": "Learn relational databases and MySQL queries.",
    "MongoDB": "Learn document databases, collections and MongoDB queries.",
    "Linux": "Learn Linux commands, files, permissions and process basics.",
}


def generate_roadmap(missing_skills):
    return [
        LEARNING_RESOURCES.get(
            skill,
            f"Learn the fundamentals of {skill} and build a small project."
        )
        for skill in missing_skills
    ]
