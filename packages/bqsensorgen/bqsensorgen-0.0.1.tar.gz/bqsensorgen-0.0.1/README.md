# bqsensorgen
A sensor generator for your BigQuery queries.


```
sensor_generator(query str, desired_pattern str, timezone str)

Args
        
1. query_text (str): A .sql file;
                          
	Example: 'SELECT * FROM x.y.z'
            
2. desired_pattern (str): RegEx string containing the desired pattern to look for. Default is BigQuery Pattern.
        
	Example: ".*\..*\..*" (looks for 'project.dataset.table' pattern)
                                           
3. timezone (str): A timezone for the datetime column of the sensor query (Big Query default is UTC)
        
	Example: 'America/Sao_Paulo'

Returns:
	str : A text with the complete sensor query.
	list: A list with all the sources (project.dataset.table) found.


--------------------------------------------------------------------	

Example: sensor_generator(query_text="SELECT * FROM x.y.z", desired_pattern=".*\..*\..*", timezone="America/Sao_Paulo")
```

# How does it work?

You give it a text with your BigQuery query, and it'll spit out a BigQuery sensor query that hopefully can be checked as true or false. 

It automatically detects 'source' tables from your query and builds a sensor based on the last updated metadata from that table (BigQuery
gives out metadata base on the dataset the table is from, hence the usage of this simple library). It is
easily editable as well, so you can quickly change what you want from its returned text.



# Examples

```
from bqsensorgen.sensorgen import sensor_generator

query = """
	SELECT * 
	FROM my_project.my_dataset.my_table T1
	INNER JOIN my_project.my_dataset.my_other_table T2
	ON T1.A = T2.B
"""

sensor_query, sources = sensor_generator(query)

print(sensor_query)
print(sources)
```


# Why BigQuery?

Because BigQuery uses the following pattern for its tables: `<project>.<dataset>.<table>` 
and you can only see a table's metadata through that table's dataset's metadata.

If you somehow want a different pattern, you can pass a RegEx expression through the arguments.

# Who should use it?

Composer/Airflow users will find it most useful, specially when using sensor Operators.