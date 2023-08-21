# Created by Brendan La Cava
# v 1.1
from time import strftime
from tkinter import Label, Tk
from tkinter.constants import LEFT, RIGHT, W
from tkinter.font import BOLD
import psutil
import wmi

# Variables
temp_upper = 75
temp_middle = 65
refresh_rate = 500  # in milliseconds
label_font = ('Arial', 18)
info_font = ('Arial', 20, BOLD)
padding = 8


def update():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    sensors = w.Sensor()
    sensor_data = {
        "CPU Temperature": None,
        "CPU Utilisation": None,
        "GPU Utilisation": None,
        "GPU Temperature": None
    }
    for sensor in sensors:
        if sensor.SensorType == u'Temperature':
            if 'CPU Package' in sensor.Name:
                sensor_data["CPU Temperature"] = (int(sensor.Value))
            elif 'GPU Core' in sensor.Name:
                sensor_data["GPU Temperature"] = int(sensor.Value)
        elif sensor.SensorType == u'Load':
            if "CPU Total" in sensor.Name:
                sensor_data["CPU Utilisation"] = int(sensor.Value)
            elif "GPU Core" in sensor.Name and "Load" in sensor.SensorType:
                sensor_data["GPU Utilisation"] = int(sensor.Value)
    if sensor_data["CPU Temperature"] is not None:
        cpu_temp['text'] = f"{sensor_data['CPU Temperature']}C"
        cpu_temp['fg'] = 'red' if sensor_data['CPU Temperature'] >= temp_upper else 'orange' if sensor_data['CPU Temperature'] >= temp_middle else 'green'
    else:
        cpu_temp['text'] = '-'
        cpu_temp['fg'] = 'red'
    if sensor_data["CPU Utilisation"] is not None:
        cpu_pc['text'] = f"{sensor_data['CPU Utilisation']}%"
    if sensor_data["GPU Utilisation"] is not None:
        gpu_pc['text'] = f"{sensor_data['GPU Utilisation']}%"
    if sensor_data["GPU Temperature"] is not None:
        gpu_temp['text'] = f"{sensor_data['GPU Temperature']}C"
        gpu_temp['fg'] = 'red' if sensor_data['GPU Temperature'] >= temp_upper else 'orange' if sensor_data['GPU Temperature'] >= temp_middle else 'green'
    ram_pc['text'] = str(int(psutil.virtual_memory()[2])) + "%"
    clock_label['text'] = strftime("%H:%M:%S")
    info_window.after(refresh_rate, update)


info_window = Tk()
info_window.geometry('270x320')
info_window.title("Information Window")

# CPU
cpuu_label = Label(info_window, text="CPU utilisation",
                   font=label_font, justify=LEFT)
cpu_pc = Label(info_window, text="%", font=info_font, justify=RIGHT)
cput_label = Label(info_window, text="CPU temp", font=label_font, justify=LEFT)
cpu_temp = Label(info_window, text="C", font=info_font, justify=RIGHT)

# GPU
gpuu_label = Label(info_window, text="GPU utilisation",
                   font=label_font, justify=LEFT)
gpu_pc = Label(info_window, text="%", font=info_font, justify=RIGHT)
gput_label = Label(info_window, text="GPU temp", font=label_font, justify=LEFT)
gpu_temp = Label(info_window, text="C", font=info_font, justify=RIGHT)

# RAM
ram_label = Label(info_window, text="RAM utilisation",
                  font=label_font, justify=LEFT)
ram_pc = Label(info_window, text="%", font=info_font, justify=RIGHT)

# Time
clock_label = Label(info_window, text="", font=info_font)

cpuu_label.grid(column=0, row=1, pady=padding, padx=padding, sticky=W)
cpu_pc.grid(column=1, row=1, pady=padding, padx=padding, sticky=W)
cput_label.grid(column=0, row=2, pady=padding, padx=padding, sticky=W)
cpu_temp.grid(column=1, row=2, pady=padding, padx=padding, sticky=W)
gpuu_label.grid(column=0, row=3, pady=padding, padx=padding, sticky=W)
gpu_pc.grid(column=1, row=3, pady=padding, padx=padding, sticky=W)
gput_label.grid(column=0, row=4, pady=padding, padx=padding, sticky=W)
gpu_temp.grid(column=1, row=4, pady=padding, padx=padding, sticky=W)
ram_label.grid(column=0, row=5, pady=padding, padx=padding, sticky=W)
ram_pc.grid(column=1, row=5, pady=padding, padx=padding, sticky=W)
clock_label.grid(columnspan=2, row=6)

update()
info_window.mainloop()
