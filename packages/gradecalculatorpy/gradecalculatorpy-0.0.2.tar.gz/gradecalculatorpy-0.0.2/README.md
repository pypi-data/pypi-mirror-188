# gradecalculatorpy

## Summary

This python package calculates grades for a course. The package allows users to customize their own course information with self-defined course component names, to update grades for different course components, and even understand how well the final exam needs to be to pass the course or achieve a target final grade.

## Functions

This package contains the following functions:

- `construct_course`: Allow users to input the information for one course component (for example, assignment name and corresponding weight) one by one. Saves the course information as a .csv file to the specified file path. (Note: any user self-defined course component name(s) can be accepted)
    - **Note**: Since this function accepts user interaction input when calling the function, developer team had not yet found a way to pass the function unit test through *pytest*.<br>
    The unit test scenarios covered in the `test_construct_course()` is based on the assumption that the input .csv file is successfully generated through a local testing by calling `construct_course('dsci524', '/')` for example

- `update_grades`: Allow users to update course component grade(s) by loading a certain saved course .csv file. The function can then save the updated course information as a new .csv file to the specified file path.
  
- `predict_final`: Calculate how well the final exam has to be in order to pass the course or achieve a certain grade just before the final exam (for the scenario only when the final grade is missing), based on the provided other course component information.

- `calculate_grade`: When all course components are presented, calculate the course overall grade based on information provided. 

## Suitability within Python Ecosystem

This course grade calculator is unique as it provides an interactive way for users to input the course component information and update information as needed. With the `predict_final` function available, users can understand how well the final exam has to be in order to pass the course or achieve a certain level of grade in this course, then adjust their final review plans based on our calculation, to meet the course expectation.

The package `predict_final` function does not take any users' previous study or course information into account to calculation of the desired final performance, only based on the current course component information inputted/updated. 

There are other course grade calculators in the Python ecosystem. Some of the examples can be found [here](https://pypi.org/project/grade/) and [here](https://pypi.org/project/grade-tracker/). While other packages focus on auto-grading without user interaction and they do not provide similar functions like `predict_final` function in this package.

## Installation

```bash
$ pip install gradecalculatorpy
```

## Usage 

Please see the following [Jupyter Notebook](https://github.com/UBC-MDS/gradecalculatorpy/blob/main/docs/example.ipynb) for a full walk-through of how to use `gradecalculatorpy`.

```
# import statements 
from gradecalculatorpy.construct_course import construct_course
from gradecalculatorpy.update_grades import update_assignment_grade
from gradecalculatorpy.calculate_grade import calculate_grade
from gradecalculatorpy.predict_final import predict_final
import pandas as pd

# create the grading structure of a course (follow the prompts that show up on the screen)
construct_course('dsci524', '/')

# update the grade of one component 
update_assignment_grade('dsci524.csv', 'Milestone 1', 95.25)

# find the grade needed for the final assignment if you want a target grade of 93 for the course 
predict_final('/dsci524.csv', 93)

# calculate the final grade of the course 
calculate_grade('dsci524.csv')
```

## Documentation 

Please see our official documentation on Read the Docs [here]().

## Acknowledging the use of OS

Since Windows and Mac systems have different file path naming style and we run all our pytest successfully on Mac. Therefore, we highly recommend the TA grading this assignment using Mac.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Contributors

Members of Group 20 of DSCI524 at UBC: <br> Chen Lin, Edward Yukun Zhang, Shirley Zhang

## License

`gradecalculatorpy` was created by Chen Lin, Edward Yukun Zhang, Shirley Zhang. It is licensed under the terms of the MIT license.

## Credits

`gradecalculatorpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
