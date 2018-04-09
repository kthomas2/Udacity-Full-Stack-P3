## Logs Analysis Project

Udacity - Full Stack Web Developer Nanodegree

Project 3: Build a reporting tool that will use information ffrom the database to discover what kind of articles the site's readers like.

### How to run

1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads) for your operating system.

2. Use Github to clone the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

3. Using your terminal, cd into the vagrant directory, run ```vagrant up```, then log into it with ```vagrant ssh```.

4. Clone the GitHub repository inside the vagrant folder. 

5. Download and unzip the data file [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and put this file into the vagrant directory. Using the terminal, cd into the vagrant directory and use the command ```psql -d news -f newsdata.sql``` to create the tables and populate them with data.

6. Create the database views log_view and failed_requests_view user the CREATE VIEW statements in the Database Views section below. 

7. Run the python3 file logs_analysis.py.


### Database Views

**log_view**

```
create view log_view as
select id, case when status = '200 OK' then '1' else '0' end as log_status,
to_char(time,'FMMonth DD, YYYY') as log_date from log;

```

**failed_requests_view**

```
create view failed_requests_view as
select f.log_date, f.total, (100.0 * f.total / a.total)::numeric(5,2) as failed_pct
from (select log_date, count(*) as total from log_view group by log_date) as a,
     (select log_date, count(*) as total from log_view where log_status = '0' group by log_date) as f
where a.log_date = f.log_date;

```