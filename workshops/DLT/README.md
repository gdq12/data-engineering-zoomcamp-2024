### Background info 

- details can be found in [material_from_repo](material_from_repo)

### Homework Answer 

1. What is the sum of the outputs of the generator for limit = 5?

    * code 
        ```{python}
        def square_root_generator(limit):
            n = 1
            while n <= limit:
                yield n ** 0.5
                n += 1

        # Example usage:
        limit = 5
        generator = square_root_generator(limit)

        total = 0
        for sqrt_value in generator:
            total = total + sqrt_value

        print(total)
        ```
    
    * answer: `8.382332347441762`

2. What is the 13th number yielded by the generator?

    * code:

        ```{python}
        def square_root_generator(limit):
            n = 1
            while n <= limit:
                yield n ** 0.5
                n += 1

        # Example usage:
        limit = 13
        generator = square_root_generator(limit)

        for sqrt_value in generator:
            print(sqrt_value)
        ```

    * answer: `3.605551275463989`

3. Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.

    * code: 

        ```{python}
        import dlt
        import duckdb

        # loading the data to duckdb
        gen_pipe = dlt.pipeline(destination = 'duckdb', dataset_name = 'generators')

        def people_1():
            for i in range(1, 6):
                yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

        def people_2():
            for i in range(3, 9):
                yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}

        info = gen_pipe.run(people_1(),
                            table_name = 'people_25_up',
                            write_disposition = 'append')

        print(info)

        info = gen_pipe.run(people_2(),
                            table_name = 'people_30_up',
                            write_disposition = 'append')

        print(info)


        # then query the imported data 

        ## establish connection with duckdb
        conn = duckdb.connect(f"{gen_pipe.pipeline_name}.duckdb")

        conn.sql(f"SET search_path = '{gen_pipe.dataset_name}'")

        print('Loaded tables: ')
        display(conn.sql("show tables"))

        # verify that tables loaded properly 
        ppl1 = conn.sql("select * from people_25_up").df()
        display(ppl1)

        ppl2 = conn.sql("select * from people_30_up").df()
        display(ppl2)

        # fetch the numbers needed to calculate age 
        ages = conn.sql("""select name, age from people_25_up
                        union 
                        select name, age from people_30_up""").df()

        ages['age'].sum()
        ```

    * answer: `353`

4. Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above.

    * code:

        ```{python}
        import dlt
        import duckdb

        # loading the data to duckdb
        gen_pipe = dlt.pipeline(destination = 'duckdb', dataset_name = 'generators')

        def people_1():
            for i in range(1, 6):
                yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

        def people_2():
            for i in range(3, 9):
                yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B"}

        info = gen_pipe.run(people_1(),
                            table_name = 'people_25_up',
                            write_disposition = 'replace')

        print(info)

        info = gen_pipe.run(people_2(),
                            table_name = 'people_25_up',
                            write_disposition = 'merge',
                            primary_key = 'id')

        print(info)

        # then query the imported data 

        ## establish connection with duckdb
        conn = duckdb.connect(f"{gen_pipe.pipeline_name}.duckdb")

        conn.sql(f"SET search_path = '{gen_pipe.dataset_name}'")

        print('Loaded tables: ')
        display(conn.sql("show tables"))

        # verify that tables loaded properly 
        ppl1 = conn.sql("select * from people_25_up").df()
        display(ppl1)

        # fetch the numbers needed to calculate age 
        ages = conn.sql("""select name, age from people_25_up""").df()

        ages['age'].sum()
        ```

    * answer: `266`


### Helpful Links

* Repo workshop [overview page](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/workshops/dlt.md)

* Subdirectory of workshop [material](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2024/workshops/dlt_resources)

* YT [video](https://www.youtube.com/watch?v=oLXhBM7nf2Q)