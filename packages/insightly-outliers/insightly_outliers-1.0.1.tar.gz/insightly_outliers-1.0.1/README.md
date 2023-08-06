# Individual Work 2022.2

## Insightly Outlier


The name "Insightly Outlier" was chosen for this project because it accurately describes the function of the library. The name was created by combining the words Insight - Internal Vision and outlier - anomaly. The library is designed to aid developers in exploring data and identifying outliers and anomalies, which is an essential part of understanding and making sense of data. The use of the word "Insightly" highlights the library's ability to provide valuable insights into the data, and the word "Outlier" specifically refers to the library's focus on identifying and analyzing outliers. Overall, the name "Insightly Outlier" effectively communicates the purpose of the library and its capabilities in a clear and concise manner.

## Objective

The knowledge of Software Configuration Management is fundamental in the life cycle of a software product. The techniques for management range from version control, build and environment configuration automation, automated testing, environment isolation to system deployment. Today, this entire cycle is integrated into a DevOps pipeline with Continuous Integration (CI) and Continuous Deployment (CD) stages implemented and automated.

To exercise these knowledge, this work has applied the concepts studied throughout the course in the software product contained in this repository.

The system is a python library for running customizable data pipelines in databases.

## Requirements

- Python 3.9
- poetry 1.3.2
- Docker

## Environment Preparation

### Environment Variables

To run the project, you need to copy the `.env.example` files in the metabase/config directory with the commands below:
```bash
cp metabase/config/metabase.env.example metabase/config/metabase.env
cp metabase/config/postgres.env.example metabase/config/postgres.env
cp metabase/config/mongo.env.example metabase/config/mongo.env
```

## How to execute

The project contains a Makefile with commands to execute the project.
To view the available commands, run the command below:

```bash
make help
```

### Packages

The project's packages can be found in the [Package Registry](https://gitlab.com/JonathanOliveira/trabalho-individual-2022.2/-/packages) of the repository or in the [PyPI](https://pypi.org/project/insightly-outliers/).

To install the package, run the command below:

```bash
pip install insightly-outliers --index-url https://TI-GCES:glpat-EXagzHgL_nhmG54ytWwN@gitlab.com/api/v4/projects/42373446/packages/pypi/simple
```

or
  
```bash
pip install insightly-outliers 
```

### Metabase

After execute the command `docker-up-build`, the metabase will be available in the address `http://localhost:3000`, and the credentials are:

- username: `admin@admin.com`
- password: `tigce20222`