# smo-database

Database and Analytics components for the Social Media Observatory.

The SMO database will combine data collections for several platforms in one database. Data for different platforms is separated by different postgres schemas (e.g. `twitter`).

## Start database

The file `docker-compose.yml` provides a basic postgres image with configured environment variables which can serve as a first basis for starting the db. 
Change the settings in this file, e.g. to setup new credentials.

With docker installed, run `docker-compose up` to create and start a postgres container.

## Database schema

All schemas are defined as SQLAlchemy python classes (e.g. `twitter/twitter_schema.py`). Schema classes include Postgres dialect specific configurations such as `ENUM` and schema definitions.

### Twitter

* `twitter_schema.py` contains a SQLAlchemy wrapper which can be used in python scripts to populate the database.
* `twitter_schema.png` contains an ER-diagram of the Twitter DB schema.
* `insert_example.py` provides a basic example on how to initi the database with the schema and insert a sample tweet.

![ER-diagram of the Twitter DB schema](twitter/twitter_schema.png)

#### Notes on schema design

Renamed fields:

* Column names in the tables mostly compl with the field names of the Twitter API
* Exceptions are made for coherent naming in the database

| Twitter API field | Database column name |
|-------------------|----------------------|
| tweet.id          | tweet.tweet_id       |
| tweet.author_id   | tweet.user_id        |
| user.id           | user.user_id         |

API fields, we omit:
* geo
* context_annotations (entity recognition, topic attribution)
* non-url entities (hashtags, cashtags, user mentions)

Omitted fields can still be retrieved from raw data collections for special analysis purposes.

Indexes and constraints:

* All tables have primary key indexes
* The tweets table has additional indexes on: 
  - created_at
  - user_id
  - year, month, day
* Todo: fulltext index in `text`
* We refrain from foreign key constraints and further unique indexes for performance reasons

### Types

We utilize ENUM defitions of postgres.

```
CREATE TYPE public.media_type AS ENUM ('photo', 'video', 'animated_gif');
CREATE TYPE public.reference_type AS ENUM ('retweeted', 'quoted', 'replied_to');
CREATE TYPE public.reply_settings AS ENUM ('everyone', 'mentionedUsers', 'following');
```

### TODO
* add fulltext index functionality to the posgres database

## Facebook and Instagram

Facebook and Instagram data are retrieved via the CrowdTangle API. Thus, primary user ids are ct_ids for accounts. 

## Youtube

Not implemented yet

## Telegram

Not implemented yet

## DBöS

The database of public speakers as the basis four our data collection.

### Entities 

The Table `dboes.entities` contains dboes entries of persons and organisations acting as public speakers.

### Metrics

The Table `dboes.entities` contains reputation and activity metrics for public speakers.

| Platform    | Metric name               |
|-------------|---------------------------|
| Twitter     | twitter.followers         |
| Twitter     | tweet.followees           |
| Facebook    | facebook.subscriber_count |
| Facebook    | facebook.like_count       |
| Facebook    | facebook.haha_count       |
| ...         | ...                       |

Todo:
* add columnar storage support for the metrics table to speed up performance
