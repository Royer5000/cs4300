import numpy as np

student_array = np.array(["Student1", "Student2", "Student3"])
gpa_array = np.array(["3.8", "3.6", "3.0"])

compiled_array = np.stack((student_array, gpa_array), axis = 1)

print(compiled_array)
print(compiled_array.ndim)
