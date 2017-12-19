This an example Python/Django web site for displaying evolution of some variables over time.

Right now it has a set of views for gasoline consumptions, and another one for money balances in accounts. The previous sentence might convey an idea of higher complexity than it actually has.

## Installation and running

It can be run by:

```bash
$ git clone https://github.com/isilanes/WebProgress
$ cd WebProgress/
$ python -m manage runserver localhost:8081
```

You might have to install the required python. You can do so via pip (using a virtualenv is recommended):

```bash
$ pip install -r conf/requirements.txt
```

The server can also be run with Gunicorn (edit script as appropriate):

```bash
$ bash gunicorn.sh
```

or even with Docker:

```bash
$ bash docker/build
$ bash docker/run $PWD/progress.db
```

## Example functionality

The main index has access to both sections (gasoline and accounting):

```
http://localhost:8081/
```

### Gasoline consumption

Index/data introduction:

```
http://localhost:8081/gasolina/
```

It presents one of the plots (gasoline consumption per 100 km), and a form to introduce data, with the following fields:

* date
* total kilometres
* partial kilometres (since previous refill)
* gasoline intake in current refill
* current gasoline price

There is also one view per each of the following properties:

* gasoline consumption per 100 km, vs total kms
* kms done with a full tank, vs refill number
* yearly km average, vs time
* monthly cost of gasoline, vs time

## Accounting

Index/data introduction:

```
http://localhost:8081/ahorro/
```

It presents a plot of the total registered money vs time, and a form to introduce data. Data is introduced as a date, and one field per registered account, for the amount of money.

There is also one view per registered account, showing a plot of money in the account vs time.

## Administrative view

The administrative view can be accessed at:

```
http://localhost:8081/admin
```

The dummy database provided with this repository can be manipulated there, the user/password being admin/passwd1234.

