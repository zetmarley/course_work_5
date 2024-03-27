CREATE DATABASE hh_employers;

CREATE TABLE employers
(
	employer_id SERIAL PRIMARY KEY,
    company_name varchar NOT NULL,
	open_vacancies int
);

CREATE TABLE vacancies
(
	vacancy_id SERIAL PRIMARY KEY,
    vacancy_name varchar NOT NULL,
	salary_from int,
	salary_to int,
	salary_currency varchar(10),
	city varchar,
	street varchar,
	building varchar,
	company_name varchar,
	requirement text,
	responsibility text,
	experience varchar,
	employment varchar,
	schedule varchar
);