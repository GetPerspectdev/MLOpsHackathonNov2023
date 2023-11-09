Project filters and grades meeting transcripts based on the principles listed in Crucial Conversations
It can do the following: 
1. Identify if a crucial conversation occured.
2. Identify the goal of the crucial conversation
3. Score each participant on a scale from 0 - 100
4. Give a reason for the score
5. Provide feedback on how the participant could improve.

Crucial Conversations represent critical points in a company's day to day. By detecting, reviewing, and providing feedback how critical conversations are handled, buisness can 
improve how important decisions are handled.

Response folder shows the output of the call to https://eodpp5oa91bzvad.m.pipedream.net where the JSON object is the body.

# MLOpsHackathonNov2023
## Introduction:
Perspect is a performance quantification platform that calculates a developer’s soft & hard skills. Unlike LinkedIn, our product tracks skills in real-time from a holistic set of data sources.
A source that we want to include is meetings. Right now this is an untapped source of data that we can use to better inform assessments of skills. We have a meeting bot that can join meetings and provide transcripts for meetings.
We have some real and some dummy data for meeting transcripts that are to be used for the purpose of this hackathon.

## Objectives:
* Identify a skill or insight that would be of value to engineers (what would be valuable for you?). Once identified, scope out and build a solution that takes in meeting transcript data and returns a score or summary of that skill or insight.
* Bonus points for creativity on the skill or insight, but feel free to use our example ideas:
  * Conversational score (what % of time are they listening vs talking, etc.)
  * Presentation score (how concisely expressed are their ideas, could use GPT-4 to summarize ideas of spoken word and compare with what they actually said, etc.)
* Be able to demo your solution at the end of the hackathon.

## Details:
* Data for meeting transcripts are in a public s3 bucket [meeting-transcripts](https://ml-hackathon-2023.s3.us-west-2.amazonaws.com/data/meeting-transcripts.zip).
* Teams are recommended but not required. No teams bigger than 3 people allowed.
* Submissions will be required to be pushed to Perspect’s public github repo to be considered.

## How to submit:
* Fork this repo and push your work via PR

## Intellectual Property & Code Rights:
* All code will be pushed to a public repo in Perspect’s github org, which uses the GPL-3.0 license.

## Prizes & Recognition:
* $2,500 total prizes (1st place: $1500, 2nd place: $750, 3rd place: $250)
* Perspect will be sponsoring additional hackathon/bounty work. Those in attendance showing valuable work will be invited to participate in future work.
=======
# Dagster + dbt starter kit

This starter demonstrates using Python alongside a medium-sized dbt project. It uses dbt's [`jaffle_shop`](https://github.com/dbt-labs/jaffle_shop), [`dagster-dbt`](https://docs.dagster.io/_apidocs/libraries/dagster-dbt), and [DuckDB](https://duckdb.org/).

*New to Dagster? Learn what Dagster is in [Dagster's hands-on Tutorials](https://docs.dagster.io/tutorial) or learn using dbt with Dagster in the [dbt + Dagster tutorial](https://docs.dagster.io/integrations/dbt/using-dbt-with-dagster).*

## Getting started

### Option 1: Deploying it on Dagster Cloud

The easiest way to spin up your Dagster project is to use [Dagster Cloud Serverless](https://docs.dagster.io/dagster-cloud/deployment/serverless). It provides out-of-the-box CI/CD and native branching that make development and deployment easy.

Check out [Dagster Cloud](https://dagster.io/cloud) to get started.

### Option 2: Running it locally

To download this example into your working directory, run:

```bash
dagster project from-example --example assets_dbt_python --name assets_dbt_python
```

To install this example and its Python dependencies, run:

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```
dagster dev
```

Open http://localhost:3000 with your browser to see the project.


## Learning more

### Changing the code locally

When developing pipelines locally, be sure to click the **Reload definition** button in the Dagster UI after you change the code. This ensures that Dagster picks up the latest changes you made.

You can reload the code using the **Deployment** page:
<details><summary>👈 Expand to view the screenshot</summary>

<p align="center">
    <img height="500" src="https://raw.githubusercontent.com/dagster-io/dagster/master/docs/next/public/images/quickstarts/basic/more-reload-code.png" />
</p>

</details>

Or from the left nav or on each job page:
<details><summary>👈 Expand to view the screenshot</summary>

<p align="center">
    <img height="500" src="https://raw.githubusercontent.com/dagster-io/dagster/master/docs/next/public/images/quickstarts/basic/more-reload-left-nav.png" />
</p>

</details>

### Using environment variables and secrets

Environment variables, which are key-value pairs configured outside your source code, allow you to dynamically modify application behavior depending on environment.

Using environment variables, you can define various configuration options for your Dagster application and securely set up secrets. For example, instead of hard-coding database credentials - which is bad practice and cumbersome for development - you can use environment variables to supply user details. This allows you to parameterize your pipeline without modifying code or insecurely storing sensitive data.

Check out [Using environment variables and secrets](https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets) for more info and examples.

### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Testing

Tests are in the `assets_dbt_python_tests` directory and you can run tests using `pytest`:

```bash
pytest assets_dbt_python_tests
```
