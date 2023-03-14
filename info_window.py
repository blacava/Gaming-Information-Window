#Created by Brendan La Cava
#v 1.0
from time import localtime, strftime
from tkinter import Label, Tk
from tkinter.constants import LEFT, RIGHT, W
from tkinter.font import BOLD
import psutil
import GPUtil
import wmi

#Variables
temp_upper = 75
temp_middle = 65
refresh_rate = 500 #in milliseconds
label_font = ('Arial', 18)
info_font = ('Arial', 20, BOLD)
padding = 8

def update():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    sensors = w.Sensor()
    cpu_temps = []
    for sensor in sensors:
        if sensor.SensorType==u'Temperature' and 'CPU Package' in sensor.Name:
            cpu_temps += [float(sensor.Value)]        
    cpu_temps.sort(reverse = True)
    try:
        cpu_info = int(cpu_temps[0])
    except IndexError:
        cpu_temp['text'] = '-'
        cpu_temp['fg'] = 'red'
    gpu = GPUtil.getGPUs()[0]
    gpu_util = int(gpu.load * 100)
    gpu_info = int(gpu.temperature)
    cpu_pc['text'] = str(int(psutil.cpu_percent())) + "%"
    cpu_temp['text'] = str(cpu_info) + "C"
    ram_pc['text'] = str(int(psutil.virtual_memory()[2])) + "%"
    gpu_pc['text'] = str(gpu_util) + "%"
    gpu_temp['text'] = str(gpu_info) + "C"
    clock_label['text'] = strftime("%H:%M:%S")
    if gpu_info >= temp_upper:
        gpu_temp['fg'] = 'red'
    elif gpu_info >= temp_middle:
        gpu_temp['fg'] = 'orange'
    else:
        gpu_temp['fg'] = 'green'
    if cpu_info >= temp_upper:
        cpu_temp['fg'] = 'red'
    elif cpu_info >= temp_middle:
        cpu_temp['fg'] = 'orange'
    else:
        cpu_temp['fg'] = 'green'
    info_window.after(refresh_rate, update)

info_window = Tk()
info_window.geometry('270x320')
info_window.title("Information Window")

#CPU
cpuu_label = Label(info_window, text = "CPU utilisation", font = label_font, justify = LEFT)
cpu_pc = Label(info_window, text =  "%", font = info_font, justify = RIGHT)
cput_label = Label(info_window, text = "CPU temp", font = label_font, justify = LEFT)
cpu_temp = Label(info_window, text = "C", font = info_font, justify = RIGHT)

#GPU
gpuu_label = Label(info_window, text = "GPU utilisation", font = label_font, justify = LEFT)
gpu_pc = Label(info_window, text = "%", font = info_font, justify = RIGHT)
gput_label = Label(info_window, text = "GPU temp", font = label_font, justify = LEFT)
gpu_temp = Label(info_window, text = "C", font = info_font, justify = RIGHT)

#RAM
ram_label = Label(info_window, text = "RAM utilisation", font = label_font, justify = LEFT)
ram_pc = Label(info_window, text = "%", font = info_font, justify = RIGHT)

#Time
clock_label = Label(info_window, text = "", font = info_font)

cpuu_label.grid(column = 0, row = 1, pady = padding, padx = padding, sticky = W)
cpu_pc.grid(column = 1, row = 1, pady = padding, padx = padding, sticky = W)
cput_label.grid(column = 0, row = 2, pady = padding, padx = padding, sticky = W)
cpu_temp.grid(column = 1, row = 2, pady = padding, padx = padding, sticky = W)
gpuu_label.grid(column = 0, row = 3, pady = padding, padx = padding, sticky = W)
gpu_pc.grid(column = 1, row = 3, pady = padding, padx = padding, sticky = W)
gput_label.grid(column = 0, row = 4, pady = padding, padx = padding, sticky = W)
gpu_temp.grid(column = 1, row = 4, pady = padding, padx = padding, sticky = W)
ram_label.grid(column = 0, row = 5, pady = padding, padx = padding, sticky = W)
ram_pc.grid(column = 1, row = 5, pady = padding, padx = padding, sticky = W)
clock_label.grid(columnspan = 2, row = 6)

update()
info_window.mainloop()
