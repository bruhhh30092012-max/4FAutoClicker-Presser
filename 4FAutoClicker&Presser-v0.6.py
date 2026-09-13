import os
import sys
import time
import gc
import json
import threading
import random
import re
import ctypes
from collections import deque
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

keyboard = None
mouse = None

_INPUT_LIBS_READY = threading.Event()

def _load_input_libs():
    global keyboard, mouse
    import keyboard as _keyboard
    import mouse as _mouse

    keyboard = _keyboard
    mouse = _mouse
    _INPUT_LIBS_READY.set()

ALL_KEYS = [

    *[c for c in "abcdefghijklmnopqrstuvwxyz"],
    *[str(n) for n in range(10)],
    *[f"f{n}" for n in range(1, 13)],
    "space", "enter", "esc", "tab", "backspace", "delete", "insert",
    "home", "end", "pageup", "pagedown",
    "up", "down", "left", "right",
    "shift", "shiftleft", "shiftright",
    "ctrl", "ctrlleft", "ctrlright",
    "alt", "altleft", "altright",
    "win", "winleft", "winright",
    "capslock", "numlock", "scrolllock",
    "printscreen", "pause", "menu",
    "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",
    *[f"num{n}" for n in range(10)],
    "add", "subtract", "multiply", "divide", "decimal", "separator",
]

COLOR_BG = "#f0f0f0"
COLOR_CARD = "#ffffff"
COLOR_BORDER = "#c8c8c8"
COLOR_TAB_BORDER = "#9a9a9a"
COLOR_HEADER_BG = "#3d3d3d"
COLOR_HEADER_TEXT = "#ffffff"
COLOR_TEXT = "#222222"
COLOR_MUTED = "#777777"
COLOR_START = "#e0e0e0"
COLOR_START_ACTIVE = "#cfcfcf"
COLOR_STOP = "#3d3d3d"
COLOR_STOP_ACTIVE = "#2a2a2a"
COLOR_BTN_IDLE = "#e6e6e6"
COLOR_BTN_IDLE_ACTIVE = "#d8d8d8"

COLOR_SIDEBAR_BG = "#eef0f3"
COLOR_SIDEBAR_BORDER = "#d9dbdf"
COLOR_SIDEBAR_HOVER_BG = "#e2e5ea"
COLOR_SIDEBAR_ACTIVE_BG = "#d6d9de"
COLOR_SIDEBAR_TEXT = "#5f6368"
COLOR_SIDEBAR_ACTIVE_TEXT = "#1a1a1a"
COLOR_SIDEBAR_ACCENT = "#2f6fd6"

SIDEBAR_COLLAPSED_WIDTH = 56
SIDEBAR_EXPANDED_WIDTH = 190

NAV_ICON_DATA = {
    'click': {
        'normal': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAACEUlEQVRIieWWTWsTURhGz3snCRVU"
            "8AsRQUFEggoVd7pwIS50qRgpLtKkMZNGQfAvuHMliDQ2qXGYhdimW8EfILq0KFpUcCEY8QuVipSkc6+LVC1NMplJxm58dnPnmXMu"
            "F97LwBpHghYztp1Eq5RGtrlTpcsA6QvFG2L4aNTSjFupvArCifUqpG17F5513XjmNCCCfv5nt0YfBzkg2ro6mhufNU2uuO6td348"
            "5fdyNFc4Jp56Ipgz+J+GACmJM5fNXzzalzCbtQ+D3Ac2+wFWZavW+sHYWGE4lDCTyQxppaaB9SFkv7PBQ+6lUqlEYKGxhorA3j5k"
            "rQjJdRu32IGFGDqWwzkpBBLmcpd2IyQHFQIH0+nxnT2FDeVFIWvBE2b/6rW2ObSauo4l17pBDPLh75PcFsz2bl3PyPvw24w4bcN8"
            "vljcFG+yJwp4M86bu6XS15VrbUeaaHDCYGaiECYacg6orVzzvdr+Rf5DoRZtooJ3YrUJjchCVEK0+tZTKKLno/LFsF70FLrl8lug"
            "rRg6wrNq9Wa9p3C5PDmwEOnI6CiUpcWygZcD2OZ/fv9cCSx0HGdRKTUC/OhDtmBERmq1WiOwEMCpTMwZo08BX0LIPimlTrpTpafd"
            "Cr6D71bLD02TYVr3od98akGmLRM7dKcy8ciPGfhHOJ3P78OLnRXMEYQdy5/XQT8Wj1nHmXwdlLWm+QUdW5/c/LsD1AAAAABJRU5E"
            "rkJggg=="
        ),
        'active': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAACCklEQVRIieXWS2sTURjG8f97Jg0i"
            "SlUUEcEboknHdlpd6cKFuNClYqVLV0pRe/ETFHdubBMEURFc2stW8AOIrqRJ22SIgopgREWqVlBM57xuVEKTTibptBuf1XDm5fnN"
            "HDjDwBpHog52XimljAl6MbItP5YeAPCG/CyqH3FkIn8z/SJKT6LRwJHBwq5FZBSCM4CgWvh3U/UE4BLodW/Qn8KY4fzowXdhfSb0"
            "rQaLxxeRaeAs4bshoL3YINc94B9rCewaKh428AjYElawJFtV9HHP1TmvKXDPhdfrRBkHNjSB/c1Ga+ShO1JIRgbb23/0A/tbwP5E"
            "Uol5czEyCFp3uLnopUhgz+XibpDUykEOecOlnQ1Bm4gFA0Bs0LF0reYcWkPZWG6E9Hyour4PbF9u0Crvm3rC1UjNYe7sn9lMW9u+"
            "WNorlVezt7vmq5dqttRJOicVnYjDk6RzHpisXgv9tK1G/kPQChpXeb2uGlDULMQFOiJfGoIJrB8XSMUUG4LPM+5boGawhcxO30qV"
            "G4IAit5ZqSZC3Y664Lev6+8CpVYxBb+ySe9FBt882PtTRPuA7y14CxbTVxhxf0UGAXJjbg70tMLnJrBPonJqLpOaWW4g9ODnM+4T"
            "MY4HMgmh59MC4yYw3bls+mlYZ+QfYe+af0ADe06QowI7AFS1rMY8M1anctmOl1G71jS/Ae29ni8IE6fBAAAAAElFTkSuQmCC"
        ),
    },
    'press': {
        'normal': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAABrklEQVRIie2VsUtbURTGf+caB6EK"
            "QkHEViEoiBQXM2Tr5GyXOBUSSBEzi+h4x2Lp7FseJIhL3+TqX5BRHERQAlWktEvBFjpo3nHIS3xN8mIuJFu+6bv3+zjfeedyeDDC"
            "CI6Q+MFaa25ufi7VDa8GUXws5O/8/MyVtTbsCPy4tTU7VjenwLtBhMVwHo6zfuR5vwBMq5u62R1CGMCqeZDd5sHEhDdDCIugC02W"
            "SnDcCrIDoOhXQQKgCmQVzfWrAW/bC5v2i6ij+7J/GJT9wwD0Hqg2OFVHrQMJXyhThWIpF3U6BWQLxRJA1lHrM1B4rap7Mf4BeA9M"
            "u2hoZ+nuI1WtVXwvU/G9DKo1QfYrvpcRZN9F61Y64Q2Hh9bi54vb34BcdPsP5SLiKyg/gN80xjbroE1E5YOK721C0hs2jGsRB0jH"
            "NBy0DiTt4X8QOAG9fMG1rLDxUq2+AkGOy74X9HI01kEHExhCOv+ptNbTo6Sll6E9UJBbTRi8oJ+T3uTZ01P93mSttUjJwwFw3keT"
            "jtCzcFy/dG3MWmtqd3eLoqnJgUTJ45/03Nx1/Ac8wgjOeALksNJlc3wetwAAAABJRU5ErkJggg=="
        ),
        'active': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAABqElEQVRIie2Vv2sTYQCGn/eIQkED"
            "AZeCIgTFmmgTaIZuTs66xD/DCFLsmFH8Mdwf4eJNrv4FGa+BtBWlIB0El0IUBI33OjRJkzZn7+Tc8kzfd+/H+3zfHR8HS5bkRHOz"
            "roP1ow83bV8qpFz63q/c+khXyRnhxpPd1ZF5D9wpQjYj6CcXft3vv2p8BQgmwchsFS0DMKwHo4tbk3lwEulq0bKp1FyfjEspaw6F"
            "nwIYvcaOJHo2m0jtzBlcO10cnH4wZhiH9SgO6xEwlOjFYT2S6OXJFhWnnbDc7AzaxzulbLPZ7Aw4PkX2LI/wCujZdCwegu4hV3Jl"
            "C0h7pQdxWGvFYa0FHAi247DWEmznyfII/xvTi9/o7L0Ft8fTH4JdAEMN/EXoyLgCWs2esTLWRDvh7UeQ/g1XDBsz+6p6Zn/Zs7Ok"
            "CeeweCezf86aNZkH53VlEgb2m/HdSqXZGbSNihEaVe8+3vvrqzKuZuk6ETo5REpb9zyQs/QtROLzZDy9Fr+VvBD0/7k1nTgp/Xw5"
            "lc9FXQeN4f6NZMTlIkxBiW875bVPsz/gJUty8weum8GawOUNyAAAAABJRU5ErkJggg=="
        ),
    },
    'record': {
        'normal': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAAD3UlEQVRIid2WXUxcRRTHf+fexRas"
            "bWLBNpG0RWlMSwEJm2iM8SMQNalNW5sbTbSFZZGvWpVEU/BFXjASg/pg5aO7hIIxaWj8aDSaFB60D/aBlsI21CCaaGrSaKrBiNj9"
            "uMeHvQuX5RaWxqeepzNz/nN+c+bOnRm41U0yFb4QbCr0aaLSNoydoroZQEWuGrZGDGSkr6/rp/8FWB2s32OrtIjw0ArSs4K+1R/u"
            "+fqmgIHAkTxbYn0IT7vUcygRRa4km5oPlABrXZpPfRqrDYfDf2QMPFhbW2Bo1ghogdM1pqIdczM5p4eG3ptza+vq6nKu27JXVY4K"
            "lDrd0z7MynD42M8rAgOBI3m2ETsH3APEReWNbVs2dba1tdk3Wg0Ay7LM7PW5rwnaDphJaOyB9Ep96QNtifXNw0Sf7Q93f7IcKGVD"
            "Q0MJoKOqpmEa4SRQGJesEPCMW2e6G9XB+j2IvAkgKi394e5wJjC3jY+NXi4r90eBSmBHid9/buLC6I+puLGoOpUWxx3btmVT52ph"
            "KZudufYOQgTAVFrdsflvWF1dv11NmQJQ0ecGQj0nvZIFAvU7E8JTIqJi2l/19/Z+76Wrqml4HuEjQH2YBakNtFChQYUzhbm5mZzT"
            "XkkOBetfsQ2ZEJFO4F1NGJcOBRte8tLasdnPgCggCRIVCxjHVKQo6RBJ3/qpygTpZPF3NwXer6lpvC9dPzg4OAtMJHNr8RKgIHmO"
            "86vXjFWM3WmweWgce7fXGNArAKpy1xKgouo9KAW0l417mSBL/nP3kv7ukO/2GmyL+SWQ8AjFMe0vPCcJ+QAi+tsSoGFrxHFLLKs5"
            "O33wYOjDywqvpkHjCC8PHD8+la63mprWAcUAopLK7QIiI467NmfDP/u8ZjwQ7v7AVCkSlWZRaVYjUXQi1N3lpc2O6j7gNkBt0x5O"
            "9S9a46pg41nQhxXG5/66Vu4cV6s2y7LMnPUbLwK7RPimP9T92JIKk3S73ZlF6e0bNr5+MzCA7DtyjwK7ki1td8cWbfOLY+en7y/3"
            "lwI7gMdLy8snxy+cn1wNrDrYaCF6DDBQTp0I97x9QyCAv6z0jI15AMgV5EBZuT+6/d6C7yYnJ5f9LSzLMv0PPtrqwEzgh9ga2RsZ"
            "Hf3XrfO8gIPBw1vjJIaBQqdrQpCORPTvz50TZAHU1LQuO6r7RNW9jFM+fE9kdAEvQIN3xiUrhLLf1X0diKROEJB8krd81rxCORVb"
            "I3Ufd3X96ZV3xUfUwRcbnjSVVlUeWUavInwL2t4f6jmzXL6Mn4nB4OGtCRIVKlqMymYURbgqcMk27eGB3t5fMs11a9t/JE1pPk64"
            "qtYAAAAASUVORK5CYII="
        ),
        'active': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAADmUlEQVRIid2WTWhcVRTHf+e+idTY"
            "LipUSoyUSEw7M828xC5EERFarFCLjTBYcFuy6EdeB5S2wYWbCMGmmZRKN+JK0NJYtSgKJgvtQhdqJjOdmTQNgq2VoqAbQzAz7x0X"
            "c2d4nXmmk+KqZ3U//uf87rnvvHsv3O8m7QqfzBR7fZ89GJNA2Wq9b4tS8I0zW5js+/l/AaYy5f0S6EngmTWFyhVF386fTX51T8DB"
            "Y9e3BKbyPvBSaHgFpYDwq4V0I6SADSHNJ1Wjh4qTyT/bBqaOLvSIE8wCPXZoDhjvNJsufzf52EpYu2v4h85K50MvC5xA1bXDS6bK"
            "nrl3E7/cFVjLbPV7kMeBqsBobnN8grckiFpc3dJpdRa7yq8DY4ADLFWNPtWcaazZsbaNNRgir+ay8Utrgep28aL4wHjKKy8JegHo"
            "jQXyHvBKWGfCnVSmvB/7zQRG59uEhS0/Ff8Y5E3bHXK98t7/BNpqBJjLbY5PrBdWt77fdrwDFABU9NQdjHpjYKT0hAqLtntwfipx"
            "ISrY4LFiInDMi6hq4DtfFs5tX4jSDRwvvqYqHwBqqvTUC6iRoaK7bXOl02y6HBUkNVLyAiN5VCeAM8bxr7pe+WiUNohVPwVWAQk6"
            "GrFDWyokLbnQXPr1zESYoFaBdXNAsylvYXuzPn/aXVbIA6hKfysQ2WLBt6JWrEb2NcEaUBHdF+Uj2AMCfSQCiEY51S1QXXM+cpHS"
            "+p+HtlT+sNhHo5xjJvgC8COmqhg+j/IxSrcN/nsLULRWxgippzM3H2x2/inbXwY53gStqjAyfya+2KxPHi5uVOiv5aKFFqBvnFnb"
            "3LCsfx+IWvH8VPycYpIiZETI4Egyn02cj9LGOjgAPABoTJlpJBYWuV7pCvAsIvN9t3bsssfVus2eqzlgpwrf5LOJ51syBFDVMdtw"
            "F7sW3rgXGMC1rtIJYCeAUcbCcy1V5HqlS8AQ4KvowXw2Ob0e2IBXTCvyIeCIynTubDwdnjfNDlWjh4Al6/CR65VPptMa9f/dYem0"
            "OimvOFqHAdf9SmW4WRd5AQ8eKW0LYswAvVaUBxkPOlY/y592l8Pa5OHixlqBSGMbURaNzwttXcCNQJniw/Y+GwoN/6NQqJ8gCt0C"
            "LtDRCKgy7Vcqw4Xzqb+i4t71EeV65b0qekqU59bQqwrfGmUsN5X4eq14bT8TB4+UtgUdultV+gW2CqjCbUSvxpSZH6eSN9qNdX/b"
            "v6bpWLdSedx4AAAAAElFTkSuQmCC"
        ),
    },
    'pixel': {
        'normal': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAADXklEQVRIie2VX2hbdRTHP+fepGub"
            "OidRpo8Tq2KZf2rFieAQHxT2og9BGGuaNlnT1EUpUrqn4lCQVqrClLbXpEsK4kN8EFHEF3GIbsNhpRu4MRXBp7F0s51pbXLvPT4k"
            "t2bZbbvia7+P39/5ns/vHO4f2Na2tii5laLu7u6QEWx7DmEfqu0Y7AJAuQbyqxr6Q7O431iWtfy/gLFYst015aggL4OGNun1t8In"
            "Yrpjecv6bUvAdDq9Y7FUeUOE14Gg5ytcFDiP6kI1LWHQvSD318UrIrxTWlw4VigUypsCY7HBu9VwP0d4omYVQY+LI7O53NQffhfs"
            "TiT2mAR6VDkChGv26aDYL2YymcvrAg/1999jOsZJoL06klritozkcu//5Qdq1MFU6o5gWceBBFQ30iT2/nroGjCdTu9YKlW+q01m"
            "K5KYzU7mG5v29iYfcoQXRETFdL/KWdaFxpqevmQckWnAFORMaan4jLdewytaWrbf8ta4HiwaT77mGjIvIhPAu+oY56PxgSONdfmZ"
            "6SyqyWovfbLltvCxGyaM9fc/qI5xDgggMpXPTKb8JnMNmQfMhiPHVOmYmZm8ePMFByyBw0BFHO3I5aYvGQDqGCNAALhirwRGGoMA"
            "KsYBHxiAaeMe8Ms0m+4wUASCrilHwVupqnpFodCq76ui4qqfv5HK5da1XiKia0ATYwyoAHet2jLuF3bF/BJwfI5sTPcL34z5zwRw"
            "J1DBcN6usoC5ubMLj3Z2tQFPI/L4Y51df/48d3auPjz/04/FRzq7rgo8z38Pm43w6mzG+roRFusbOIwwWp2OsfxH059SF2Rna3BU"
            "kDMAClY0nko0NpnNTn1gqnSIypCoDKnhdOQzU5M3w5IDKnj+qdLiwo1PqadEIrG7rIGTAg/UwDNBKsPZbPaq38oaFY2+EjaCzoRC"
            "T836xXCD+0+cOH7FF+hBKxr4DNhXs66BfoipufU+yofig/cFxO1V1UGQXTX7e8MNvlQP8wUCRCKRptad4VFgGGiqO/pd4JyqXgYQ"
            "kd2KPAy6p65mVZXx5oD7pmVZlcbeG/6e+vpS9zq4I4gcBNo2qgWuI/Kx2Dq23kd+U6CnSGSoJXT78rOqPCUY7Spa/SMoRVUugZxa"
            "ud78baHw3sqt9NvWtrakfwFDt0t/GndpBgAAAABJRU5ErkJggg=="
        ),
        'active': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAADPUlEQVRIie2VT0xcVRSHv3PfDFQh"
            "pgRNdeGipiMw4wyt1rTdWI0bTTe6MnHTWFttK2UgSujK0GhioKEwpSZK1KiJcWuMf3ZGYhRdVGFgGKaoMXHVFIuxCsK8e4+LeUOn"
            "rw8occtv9879nfO9c96798KWtrRJya2YMq9MNlCOPW6U/WASDt0OICILou5nFfNdbOmfry6O7l38X8DdnTMJhdMIzwANG9T6W+Fj"
            "52z/9Ej6l00Bd52aq28wK30gLwPxmqUS6DTCHwAozaikEe6v8ZQFOVtucmcKfamVDYGpk4W7Y3HzKejDQWgeZESEDyeG236LesFM"
            "x+xOE7OHnUqHQHMQ/t5in5rOpS+vCXyoa+YeXxkDEpVVHRVWeieG9/wZBQorfSLf5MVjAyocDUIliz1YC10FVsbofxN05ovK0Ynz"
            "bR+Ei+45VUg6zzyBqjrrfTl1oWX2po6zM88LvA14wA9+kz5SHa+pmho9//XqGNeCZTpnss5IHtVB4Jzx7HR7ttgR9uVzyXcVXgwe"
            "98UWOHNDh+mOUqvx7BQQA96azCVPRHZmJB+8da2sYlL5XGspotNRgWNAWZTUxPnknAEwnt8bwK5sc/HecCKAGjkUAQPwRPRQVE58"
            "W30PMA/EFU7D6kiNVk3+7SZyqzhVjYqvJ7v81/Vagq4CFekHysBd/vK/A1HJMeM+B2zEko/hs6gcdfWDwJ1A2Tr7xiown2stIQxV"
            "XPJCe1fhSDj5x+F0EaQrBPVV6Jw813Yp7N+dLR5DOFJpTs5WT5/QtiiPAfsAq8Lx/HDynXChTHa2xYh7EkCNfBEFa+8sHEfkAuAp"
            "jNsmfbS6LW74Xg9kp3Z4eGNAS6Vb3vM97SkMpa5GjSys1peKzXVxHRTlcCWdoufiB38aSVypem76QQLoJ8D+ILQAvGmdfX+tQ/nB"
            "7sIu58xzip4Etlei+q1xdU/XwiKBAKm+Qp13VV4VoQeou76iv6rIlKCXKx3IDlEywM6a9GWEgdji4msXR/eWw7XXvZ7S3ZfuM1ru"
            "ReVZoHE9L3AN+EhE+tc65DcEVnWg+/fbluy1x1Q4ACRUKzeCCPMIcw4db5Q7vh4funfpVuptaUub0n9s30BAahdYkwAAAABJRU5E"
            "rkJggg=="
        ),
    },
    'profile': {
        'normal': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAABqUlEQVRIie2VzytEURTHv+fMTBpF"
            "yWYmEXvlV0lIs1NEKWRhMYkhbOY/uP+C1NgMPbMjlijZqKlJmczGQjYyFjMlCxuT9+YdC2y8ybump5Dv8vY938+5t3vPBf7120Vf"
            "LYhGl0PC0gsAATbPkslk8VuAU1PxYLD+aY2AOQC+t2ULREmynuKGYZR0cvy6jdXWl3YAjDnqRZbEVxMCMKEVpGOKzi+OiNDBpybh"
            "4e2txLFbFusABfxxZxVUHtfJ0gKSoMHdRI2eAQX2tTsPV54BqYwUgOdPLM9sU0ony+duAXK57ENXV889iEbhvGg2iFaMzY0Tz4AA"
            "kLvInnd296QBagIhDIIFwqkIL6Q2N/Z1c/6+tB7+bCwWZpsGGNRuC5oJqHutpkexJQ+WS7Z8acNIFKoGKqX4Jl+cEcgqgD6N5kQE"
            "GSastzaHdpVStjZwNhYLs8V7ROh367iyKB0gc7LST+J4hxGl/Fzmo+phACCDJvyHEaUcn4MD2HJbjBDQUT3snYnutrvCkCuQSWNu"
            "6jLFOV+1RpuXcpyxSWYmIIFpL8JNMjNe5PzrZ+kFAhV+ZuGSLTIAAAAASUVORK5CYII="
        ),
        'active': (
            "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAABmJLR0QA/wD/AP+gvaeTAAABpklEQVRIie2VP0hbURSHv/NeMmQQ"
            "aQvWDB1cStNUDQrS2iIBh0KhnaR0LghFrCajWybXYgQnh5KlWLraQpcsSujWtE1oEaTg0i6tifQP8b17HIwgJPhu9Am1+I3vnvf7"
            "7j28ex6cc9aRTl9ITlV63SgjAAbz7tNC//dTEd7KbsV+mZ0FgceA23zsAcu1Wiz79XnfX5scx06n8tuvrwhMHpIBRIAn3d1/Xthu"
            "3OqEqZnqPRVWjywycre8mHgblGV1QhXuBxaJPrDJsmwpF4KFXApTuBHoE/0SmlCUAtA4oqThS7QQmvB9/voGqrOAtlk2ovL047Or"
            "mzZZHV38gZnKuIjMAaMAqqwLznw5f63YSc7/jVVLhzPV+C5624EbauQKIl37K1pXlS0cU/EbrFWWkt+OL8ypk/r5+ZFBpwVuWmxO"
            "gZIqix8uJl6SE2MtHM5U457yiubHcQzWfPyJdn+SlmuRzhUjHvLmBDKAOy7u63SuGAkU1mqX06gOnkB2wNCP7Z6xQKEaDZ6bljja"
            "Ol9tZ2lotPTYGK/kOJGHYYQb45XCyDnn32IPRsiBRyHAomwAAAAASUVORK5CYII="
        ),
    },
}

SMART_CLICK_RADIUS = 5
MEMORY_CLEANUP_THRESHOLD_MB = 40
DEFAULT_MOVE_RECORD_INTERVAL_MS = 100
MIN_MOVE_RECORD_INTERVAL_MS = 10
MULTI_CLICK_GAP_S = 0.02
WHEEL_TICK_GAP_S = 0.1
RECORD_BLANK_ROW_IID = "__blank__"

TAP_MAX_DURATION_S = 0.05

RECORD_CTX_ATTRS = (
    'recording', 'recorded_events', 'record_start_time', '_keys_held', '_buttons_held',
    '_last_move_record_wall', '_record_row_map', '_count_label_update_pending',
    'playing', 'playback_thread',
    'record_tree', 'record_count_label', 'record_toggle_btn', 'playback_toggle_btn',
    'record_moves_var', 'record_keys_var', 'record_move_interval_entry',
    'playback_repeat_mode_var', 'playback_repeat_entry', 'playback_speed_entry',
)

if hasattr(ctypes, "windll"):
    class _PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_uint32),
            ("PageFaultCount", ctypes.c_uint32),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    ctypes.windll.user32.GetDC.restype = ctypes.c_void_p
    ctypes.windll.user32.GetDC.argtypes = [ctypes.c_void_p]
    ctypes.windll.user32.ReleaseDC.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    ctypes.windll.gdi32.GetPixel.restype = ctypes.c_uint32
    ctypes.windll.gdi32.GetPixel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

def get_process_memory_mb():
    if not hasattr(ctypes, "windll"):
        return 0.0
    try:
        counters = _PROCESS_MEMORY_COUNTERS()
        counters.cb = ctypes.sizeof(_PROCESS_MEMORY_COUNTERS)
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
        return counters.WorkingSetSize / (1024 * 1024)
    except Exception:
        return 0.0

COLOR_SECTION_BG = "#ffffff"
COLOR_SECTION_BORDER = "#dcdcdc"
COLOR_SECTION_TITLE = "#555555"
COLOR_SCROLL_TROUGH = "#e8e8e8"
COLOR_SCROLL_THUMB = "#b5b5b5"
COLOR_SCROLL_THUMB_ACTIVE = "#8f8f8f"

BACKGROUND_WIDGET_CLASSES = {"Frame", "TFrame", "Label", "TLabel", "Canvas", "TLabelframe", "Toplevel"}

class RateCounter:
    def __init__(self, window=1.0):
        self.window = window
        self._times = deque()
        self._lock = threading.Lock()

    def tick(self, n=1):
        now = time.time()
        with self._lock:
            for _ in range(max(1, n)):
                self._times.append(now)
            cutoff = now - self.window
            while self._times and self._times[0] < cutoff:
                self._times.popleft()

    def rate(self):
        now = time.time()
        with self._lock:
            cutoff = now - self.window
            while self._times and self._times[0] < cutoff:
                self._times.popleft()
            return len(self._times) / self.window

    def reset(self):
        with self._lock:
            self._times.clear()

class PixelWatcher:

    def __init__(self, watcher_id, title=None):
        self.id = watcher_id
        self.title = title or f"Watcher {watcher_id}"
        self.frame = None
        self.window = None
        self.card = None
        self.card_title_label = None
        self.card_toggle_btn = None

        self.running = False
        self.gen = 0
        self.stop_event = None
        self.thread = None

        self.recording = False
        self.recorded_events = []
        self.record_start_time = 0.0
        self._keys_held = set()
        self._buttons_held = set()
        self._last_move_record_wall = 0.0
        self._record_row_map = []
        self._count_label_update_pending = False
        self.playing = False
        self.playback_thread = None
        self.record_tree = None
        self.record_count_label = None
        self.record_toggle_btn = None
        self.playback_toggle_btn = None
        self.record_moves_var = None
        self.record_keys_var = None
        self.record_move_interval_entry = None
        self.playback_repeat_mode_var = None
        self.playback_repeat_entry = None
        self.playback_speed_entry = None
        self.record_hotkey_entry = None
        self.playback_hotkey_entry = None

        self.x_entry = None
        self.y_entry = None
        self.pick_btn = None
        self.preview_swatch = None
        self.preview_hex_entry = None
        self.preview_r_entry = None
        self.preview_g_entry = None
        self.preview_b_entry = None
        self.mode_var = None
        self.target_frame = None
        self.target_swatch = None
        self.target_hex_entry = None
        self.target_r_entry = None
        self.target_g_entry = None
        self.target_b_entry = None
        self.tolerance_entry = None
        self.interval_entry = None
        self.cooldown_entry = None
        self.stop_after_trigger_var = None
        self.hotkey_entry = None
        self.toggle_btn = None

    @property
    def hotkey_which(self):
        return f"pixel_watch_{self.id}"

class AutoClickerPresser:
    def __init__(self, root):
        self.root = root
        self.root.title("4FAuto")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        try:
            myappid = 'mycompany.autoclicker.presser.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        try:
            if getattr(sys, 'frozen', False):
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))

            icon_path = os.path.join(base_path, "logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        try:
            if getattr(sys, 'frozen', False):
                settings_dir = os.path.dirname(sys.executable)
            else:
                settings_dir = os.path.dirname(os.path.abspath(__file__))
        except Exception:
            settings_dir = os.getcwd()
        self.settings_path = os.path.join(settings_dir, "4FAutoClicker_settings.json")
        self.profiles_path = os.path.join(settings_dir, "4FAutoClicker_profiles.json")
        self.profiles = {}
        self.active_profile_name = None

        style = ttk.Style()
        style.theme_use('clam')

        self.root.option_add("*TRadiobutton.takeFocus", 0)
        self.root.option_add("*TCheckbutton.takeFocus", 0)

        style.configure("TLabel", background=COLOR_CARD, foreground=COLOR_TEXT, font=("Segoe UI", 9))
        style.configure("Muted.TLabel", background=COLOR_CARD, foreground=COLOR_MUTED, font=("Segoe UI", 8))
        style.configure("TRadiobutton", background=COLOR_CARD, foreground=COLOR_TEXT)
        style.configure("TCheckbutton", background=COLOR_CARD, foreground=COLOR_TEXT)
        style.layout("Round.TCheckbutton", style.layout("TRadiobutton"))
        style.configure("Round.TCheckbutton", background=COLOR_CARD, foreground=COLOR_TEXT)
        style.configure("TEntry", padding=2, fieldbackground=COLOR_CARD, foreground=COLOR_TEXT)
        style.map("TEntry",
                  fieldbackground=[("readonly", COLOR_CARD), ("disabled", "#eeeeee")],
                  foreground=[("readonly", COLOR_TEXT), ("disabled", COLOR_MUTED)])

        style.configure("TCombobox", padding=2, fieldbackground=COLOR_CARD, background=COLOR_CARD,
                         foreground=COLOR_TEXT, arrowcolor=COLOR_TEXT, selectbackground=COLOR_CARD,
                         selectforeground=COLOR_TEXT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", COLOR_CARD), ("disabled", "#eeeeee")],
                  background=[("readonly", COLOR_CARD), ("active", COLOR_CARD)],
                  foreground=[("readonly", COLOR_TEXT), ("disabled", COLOR_MUTED)])

        style.configure("Modern.Vertical.TScrollbar",
                         gripcount=0,
                         background=COLOR_SCROLL_THUMB,
                         darkcolor=COLOR_SCROLL_THUMB,
                         lightcolor=COLOR_SCROLL_THUMB,
                         troughcolor=COLOR_SCROLL_TROUGH,
                         bordercolor=COLOR_SCROLL_TROUGH,
                         arrowcolor=COLOR_MUTED,
                         arrowsize=12,
                         relief="flat",
                         borderwidth=0,
                         width=12)
        style.map("Modern.Vertical.TScrollbar",
                  background=[("active", COLOR_SCROLL_THUMB_ACTIVE), ("pressed", COLOR_SCROLL_THUMB_ACTIVE)],
                  darkcolor=[("active", COLOR_SCROLL_THUMB_ACTIVE), ("pressed", COLOR_SCROLL_THUMB_ACTIVE)],
                  lightcolor=[("active", COLOR_SCROLL_THUMB_ACTIVE), ("pressed", COLOR_SCROLL_THUMB_ACTIVE)])

        style.configure("TNotebook", background=COLOR_BG, borderwidth=1,
                         bordercolor=COLOR_TAB_BORDER, tabmargins=[4, 6, 4, 0])
        style.configure("TNotebook.Tab", background=COLOR_BTN_IDLE, foreground=COLOR_TEXT,
                         font=("Segoe UI", 9, "bold"), padding=[16, 5], borderwidth=1,
                         bordercolor=COLOR_TAB_BORDER, lightcolor=COLOR_BTN_IDLE, darkcolor=COLOR_BTN_IDLE)
        style.map("TNotebook.Tab",
                  background=[("selected", COLOR_CARD), ("active", COLOR_BTN_IDLE_ACTIVE)],
                  foreground=[("selected", COLOR_TEXT), ("active", COLOR_TEXT)],
                  lightcolor=[("selected", COLOR_CARD)],
                  darkcolor=[("selected", COLOR_CARD)],
                  bordercolor=[("selected", COLOR_TAB_BORDER)],
                  padding=[("selected", [16, 8]), ("!selected", [16, 5])],
                  expand=[("selected", [1, 1, 1, 0])])

        style.configure("Record.Treeview",
                         background=COLOR_BG,
                         fieldbackground=COLOR_BG,
                         foreground=COLOR_TEXT,
                         font=("Segoe UI", 9),
                         rowheight=22,
                         borderwidth=0,
                         relief="flat")
        COLOR_TREE_HEAD_BG = "#e9e9e9"
        COLOR_TREE_HEAD_TEXT = "#000000"
        style.configure("Record.Treeview.Heading",
                         background=COLOR_TREE_HEAD_BG,
                         foreground=COLOR_TREE_HEAD_TEXT,
                         font=("Segoe UI", 8, "bold"),
                         relief="flat",
                         borderwidth=0)
        style.map("Record.Treeview",
                  background=[("selected", "#d6d6d6")],
                  foreground=[("selected", COLOR_TEXT)])
        style.map("Record.Treeview.Heading",
                  background=[("active", COLOR_TREE_HEAD_BG), ("pressed", COLOR_TREE_HEAD_BG)],
                  foreground=[("active", COLOR_TREE_HEAD_TEXT), ("pressed", COLOR_TREE_HEAD_TEXT)])
        style.layout("Record.Treeview", style.layout("Treeview"))

        self.root.option_add("*TCombobox*Listbox.background", COLOR_CARD)
        self.root.option_add("*TCombobox*Listbox.foreground", COLOR_TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#d6d6d6")
        self.root.option_add("*TCombobox*Listbox.selectForeground", COLOR_TEXT)
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 9))

        self.clicker_running = False
        self.presser_running = False
        self.clicker_gen = 0
        self.clicker_stop_event = None
        self.presser_gen = 0
        self.presser_stop_event = None
        self.pixel_watchers = []
        self._pixel_watcher_next_id = 1
        self.capturing_hotkey_for = None
        self._hotkey_capture_hook = None
        self._hotkey_capture_prev_value = None
        self._hotkey_capture_timeout_id = None
        self.hotkey_specs = {}

        self.recording = False
        self.playing = False
        self.recorded_events = []
        self._action_clipboard = None
        self.record_start_time = 0.0
        self._record_row_map = []
        self._keys_held = set()
        self._buttons_held = set()
        self._last_move_record_wall = 0.0
        self._count_label_update_pending = False

        self._active_record_owner = None
        self._global_record_store = {}

        self.clicker_thread = None
        self.presser_thread = None
        self.playback_thread = None

        self.click_rate_counter = RateCounter()
        self.press_rate_counter = RateCounter()
        self._last_click_cps_text = "Current CPS: 0.0"
        self._last_press_pps_text = "Current PPS: 0.0"

        self.presser_paused = False
        self.presser_awaiting_target = False
        self._press_block_handle = None

        self._active_scroll_canvas = None
        self.root.bind_all("<MouseWheel>", self._route_mousewheel)
        self.root.bind_all("<Button-4>", self._route_mousewheel_linux_up)
        self.root.bind_all("<Button-5>", self._route_mousewheel_linux_down)

        self.create_scrollable_container()
        self.create_widgets(self.scroll_frame)

        self.root.update_idletasks()
        self.fit_window_to_screen()

        self.hotkey_thread = threading.Thread(target=self.listen_hotkeys, daemon=True)
        self.hotkey_thread.start()

        self.memory_watchdog_thread = threading.Thread(target=self.watch_memory, daemon=True)
        self.memory_watchdog_thread.start()

        self.root.bind_all("<Button-1>", self._on_global_click, add="+")
        self.root.after(0, self._build_remaining_tabs)
        self.root.after(150, self.update_rate_labels)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _canvas_can_scroll(self, canvas):
        lo, hi = canvas.yview()
        return (hi - lo) < 0.999

    def _route_mousewheel(self, event):
        c = self._active_scroll_canvas
        if c is not None and self._canvas_can_scroll(c):
            c.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _route_mousewheel_linux_up(self, event):
        c = self._active_scroll_canvas
        if c is not None and self._canvas_can_scroll(c):
            c.yview_scroll(-1, "units")

    def _route_mousewheel_linux_down(self, event):
        c = self._active_scroll_canvas
        if c is not None and self._canvas_can_scroll(c):
            c.yview_scroll(1, "units")

    def _register_scrollable(self, canvas):
        def _enter(e):
            self._active_scroll_canvas = canvas

        def _leave(e):
            if self._active_scroll_canvas is canvas:
                self._active_scroll_canvas = None

        canvas.bind("<Enter>", _enter)
        canvas.bind("<Leave>", _leave)

    def _make_scroll_area(self, parent, bg, height=None):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        if height is not None:
            canvas.configure(height=height)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview,
                                   style="Modern.Vertical.TScrollbar")
        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=bg)
        inner_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        state = {'pending': False, 'width': -1}

        def _apply_scrollregion():
            state['pending'] = False
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_inner_configure(e):
            if not state['pending']:
                state['pending'] = True
                self.root.after_idle(_apply_scrollregion)

        def _on_canvas_configure(e):
            if e.width == state['width']:
                return
            state['width'] = e.width
            canvas.itemconfig(inner_window, width=e.width)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        self._register_scrollable(canvas)

        return canvas, scrollbar, inner

    def create_scrollable_container(self):
        self.canvas, self.v_scrollbar, self.scroll_frame = self._make_scroll_area(self.root, COLOR_BG)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

    def fit_window_to_screen(self):
        req_width = self.scroll_frame.winfo_reqwidth() + self.v_scrollbar.winfo_reqwidth() + 4
        req_height = self.scroll_frame.winfo_reqheight()

        screen_h = self.root.winfo_screenheight()
        max_height = screen_h - 120
        final_height = min(req_height, max_height)

        self.root.geometry(f"{req_width}x{final_height}")

    def make_section(self, parent, title):
        wrap = tk.Frame(parent, bg=COLOR_SECTION_BORDER, bd=0)
        wrap.pack(fill="x", pady=(0, 8))

        inner = tk.Frame(wrap, bg=COLOR_SECTION_BG, padx=10, pady=8)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        if title:
            tk.Label(inner, text=title.upper(), bg=COLOR_SECTION_BG, fg=COLOR_SECTION_TITLE,
                      font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 6))

        return inner

    def create_widgets(self, parent):
        main_frame = tk.Frame(parent, padx=12, bg=COLOR_BG)
        main_frame.pack(fill="both", expand=True, pady=(4, 12))

        body_frame = tk.Frame(main_frame, bg=COLOR_BG)
        body_frame.pack(fill="both", expand=True)

        sidebar_space = tk.Frame(body_frame, bg=COLOR_SIDEBAR_BG, width=SIDEBAR_COLLAPSED_WIDTH)
        sidebar_space.pack(side="left", fill="y")
        sidebar_space.pack_propagate(False)

        self.content_area = tk.Frame(body_frame, bg=COLOR_CARD, highlightthickness=1,
                                      highlightbackground=COLOR_BORDER)
        self.content_area.pack(side="left", fill="both", expand=True)
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        click_tab = tk.Frame(self.content_area, bg=COLOR_CARD, padx=10, pady=10)
        press_tab = tk.Frame(self.content_area, bg=COLOR_CARD, padx=10, pady=10)
        record_tab = tk.Frame(self.content_area, bg=COLOR_CARD, padx=10, pady=10)
        pixel_watch_tab = tk.Frame(self.content_area, bg=COLOR_CARD, padx=10, pady=10)
        profile_tab = tk.Frame(self.content_area, bg=COLOR_CARD, padx=10, pady=10)

        for frame in (click_tab, press_tab, record_tab, pixel_watch_tab, profile_tab):
            frame.grid(row=0, column=0, sticky="nsew")

        nav_defs = [
            ("click", "Mouse Clicker", click_tab),
            ("press", "Key Presser", press_tab),
            ("record", "Record & Playback", record_tab),
            ("pixel", "Pixel Watcher", pixel_watch_tab),
            ("profile", "Profile", profile_tab),
        ]

        # Overlay nav panel: placed (not packed) so expanding it draws on top of
        # content_area instead of pushing/resizing the rest of the layout.
        sidebar = tk.Frame(body_frame, bg=COLOR_SIDEBAR_BG,
                            highlightthickness=1, highlightbackground=COLOR_SIDEBAR_BORDER)
        sidebar.place(x=0, y=0, width=SIDEBAR_COLLAPSED_WIDTH, relheight=1.0)
        sidebar.pack_propagate(False)
        sidebar.lift()

        self._build_sidebar_nav(sidebar, nav_defs)

        self.build_click_tab(click_tab)

        self._press_tab = press_tab
        self._record_tab = record_tab
        self._pixel_watch_tab = pixel_watch_tab
        self._profile_tab = profile_tab
        self._remaining_tabs_built = False

        self._select_nav_tab("click")

    def _load_nav_icons(self):
        if hasattr(self, '_nav_icon_images'):
            return self._nav_icon_images
        images = {}
        for key, states in NAV_ICON_DATA.items():
            images[key] = {
                state: tk.PhotoImage(data=b64_str)
                for state, b64_str in states.items()
            }
        self._nav_icon_images = images
        return images

    def _build_sidebar_nav(self, sidebar, nav_defs):
        self._sidebar = sidebar
        self._sidebar_expanded = False
        self._nav_items = []
        icons = self._load_nav_icons()

        toggle_row = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG, height=SIDEBAR_COLLAPSED_WIDTH, cursor="hand2")
        toggle_row.pack(fill="x")
        toggle_row.pack_propagate(False)
        toggle_box = tk.Frame(toggle_row, bg=COLOR_SIDEBAR_BG, width=SIDEBAR_COLLAPSED_WIDTH,
                               height=SIDEBAR_COLLAPSED_WIDTH, cursor="hand2")
        toggle_box.pack(side="left")
        toggle_box.pack_propagate(False)
        self._sidebar_toggle_btn = tk.Label(toggle_box, text=">", bg=COLOR_SIDEBAR_BG,
                                             fg=COLOR_SIDEBAR_TEXT, font=("Segoe UI", 15, "bold"), cursor="hand2")
        self._sidebar_toggle_btn.pack(expand=True)
        for widget in (toggle_row, toggle_box, self._sidebar_toggle_btn):
            widget.bind("<Button-1>", lambda e: self._toggle_sidebar())

        tk.Frame(sidebar, bg=COLOR_SIDEBAR_BORDER, height=1).pack(fill="x")

        for key, label, frame in nav_defs:
            row = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG, cursor="hand2", height=SIDEBAR_COLLAPSED_WIDTH)
            row.pack(fill="x")
            row.pack_propagate(False)

            icon_box = tk.Frame(row, bg=COLOR_SIDEBAR_BG, width=SIDEBAR_COLLAPSED_WIDTH,
                                 height=SIDEBAR_COLLAPSED_WIDTH, cursor="hand2")
            icon_box.pack(side="left")
            icon_box.pack_propagate(False)

            icon_label = tk.Label(icon_box, image=icons[key]['normal'], bg=COLOR_SIDEBAR_BG, cursor="hand2")
            icon_label.pack(expand=True)

            text_label = tk.Label(row, text=label, bg=COLOR_SIDEBAR_BG, fg=COLOR_SIDEBAR_TEXT,
                                   font=("Segoe UI", 10), anchor="w", cursor="hand2")

            item = {'key': key, 'row': row, 'icon_box': icon_box, 'icon_label': icon_label,
                    'text_label': text_label, 'frame': frame}
            self._nav_items.append(item)

            for widget in (row, icon_box, icon_label, text_label):
                widget.bind("<Button-1>", lambda e, k=key: self._select_nav_tab(k))
                widget.bind("<Enter>", lambda e, it=item: self._on_nav_hover(it, True))
                widget.bind("<Leave>", lambda e, it=item: self._on_nav_hover(it, False))

    def _toggle_sidebar(self):
        self._sidebar_expanded = not self._sidebar_expanded
        new_width = SIDEBAR_EXPANDED_WIDTH if self._sidebar_expanded else SIDEBAR_COLLAPSED_WIDTH
        self._sidebar.place_configure(width=new_width)
        self._sidebar.lift()
        self._sidebar_toggle_btn.configure(text="<" if self._sidebar_expanded else ">")

        for item in self._nav_items:
            if self._sidebar_expanded:
                item['text_label'].pack(side="left", fill="both", expand=True, padx=(2, 10))
            else:
                item['text_label'].pack_forget()

    def _on_nav_hover(self, item, hovering):
        if item['key'] == getattr(self, '_active_nav_key', None):
            return
        bg = COLOR_SIDEBAR_HOVER_BG if hovering else COLOR_SIDEBAR_BG
        item['row'].configure(bg=bg)
        item['icon_box'].configure(bg=bg)
        item['icon_label'].configure(bg=bg)
        item['text_label'].configure(bg=bg)

    def _select_nav_tab(self, key):
        self._active_nav_key = key
        for item in self._nav_items:
            active = item['key'] == key
            bg = COLOR_SIDEBAR_ACTIVE_BG if active else COLOR_SIDEBAR_BG
            item['row'].configure(bg=bg)
            item['icon_box'].configure(bg=bg)
            item['icon_label'].configure(bg=bg)
            item['text_label'].configure(bg=bg)
            if active:
                item['frame'].tkraise()
        self._on_tab_changed()

    def _on_tab_changed(self, event=None):
        self._build_remaining_tabs()

        def _fix_focus():
            stray = self.root.focus_get()
            if stray is not None:
                try:
                    stray.selection_clear()
                except Exception:
                    pass
            self.root.focus_set()

        self.root.after_idle(_fix_focus)

    def _build_remaining_tabs(self):
        if self._remaining_tabs_built:
            return
        self._remaining_tabs_built = True
        self.build_press_tab(self._press_tab)
        self.build_record_tab(self._record_tab)
        self.build_pixel_watch_tab(self._pixel_watch_tab)
        self.build_profile_tab(self._profile_tab)
        self.root.update_idletasks()
        self.fit_window_to_screen()
        self.load_profiles_store()

    def build_click_tab(self, click_body):
        click_timing_section = self.make_section(click_body, "Timing")
        self.click_int_vars = self.create_interval_row(click_timing_section, "Click interval")

        opts_section = self.make_section(click_body, "Click Options")
        opts_frame = tk.Frame(opts_section, bg=COLOR_CARD)
        opts_frame.pack(fill="x")

        ttk.Label(opts_frame, text="Mouse button:").grid(row=0, column=0, sticky="w", padx=(0, 4), pady=2)
        self.mouse_btn_var = tk.StringVar(value="Left")
        ttk.Combobox(opts_frame, textvariable=self.mouse_btn_var, values=["Left", "Right", "Middle"],
                     width=8, state="readonly").grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(opts_frame, text="Click type:").grid(row=0, column=2, sticky="w", padx=(16, 4), pady=2)
        self.click_type_var = tk.StringVar(value="Single")
        ttk.Combobox(opts_frame, textvariable=self.click_type_var, values=["Single", "Double", "Triple"],
                     width=8, state="readonly").grid(row=0, column=3, sticky="w", pady=2)

        ttk.Label(opts_frame, text="Action mode:").grid(row=0, column=4, sticky="w", padx=(16, 4), pady=2)
        self.click_action_mode_var = tk.StringVar(value="Click")
        ttk.Combobox(opts_frame, textvariable=self.click_action_mode_var, values=["Click", "Hold"],
                     width=8, state="readonly").grid(row=0, column=5, sticky="w", pady=2)

        self.smart_click_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts_frame, text="Smart click", variable=self.smart_click_var,
                        style="Round.TCheckbutton").grid(
            row=1, column=2, columnspan=4, sticky="w", padx=(24, 0), pady=(6, 0))

        self.click_max_speed_var = tk.BooleanVar(value=False)
        max_cps_row = tk.Frame(opts_frame, bg=COLOR_CARD)
        max_cps_row.grid(row=3, column=0, columnspan=6, sticky="w", pady=(6, 0))
        ttk.Checkbutton(max_cps_row, text="Max CPS:",
                         variable=self.click_max_speed_var,
                         command=self.on_click_max_speed_toggle).pack(side="left")
        self.click_max_cps_entry = ttk.Entry(max_cps_row, width=6, justify="right", state="disabled")
        self.click_max_cps_entry.insert(0, "10")
        self.click_max_cps_entry.pack(side="left", padx=6)
        ttk.Label(max_cps_row, text="CPS").pack(side="left")
        self.click_cps_label = ttk.Label(max_cps_row, text="Current CPS: 0.0", style="Muted.TLabel")
        self.click_cps_label.pack(side="left", padx=(16, 0))

        self.repeat_mode_var = tk.StringVar(value="infinite")
        ttk.Radiobutton(opts_frame, text="Repeat until stopped", variable=self.repeat_mode_var,
                         value="infinite").grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))
        repeat_frame = tk.Frame(opts_frame, bg=COLOR_CARD)
        repeat_frame.grid(row=2, column=0, columnspan=4, sticky="w", pady=2)
        ttk.Radiobutton(repeat_frame, text="Repeat click", variable=self.repeat_mode_var, value="finite").pack(side="left")
        self.repeat_entry = ttk.Entry(repeat_frame, width=6)
        self.repeat_entry.insert(0, "100")
        self.repeat_entry.pack(side="left", padx=5)
        ttk.Label(repeat_frame, text="times").pack(side="left")

        pos_section = self.make_section(click_body, "Cursor Position")
        pos_frame = tk.Frame(pos_section, bg=COLOR_CARD)
        pos_frame.pack(fill="x")

        ttk.Label(pos_frame, text="Cursor position:").grid(row=0, column=0, sticky="w", pady=2)
        self.pos_mode_var = tk.StringVar(value="current")
        ttk.Radiobutton(pos_frame, text="Current location", variable=self.pos_mode_var, value="current").grid(
            row=1, column=0, columnspan=3, sticky="w")

        pick_row = tk.Frame(pos_frame, bg=COLOR_CARD)
        pick_row.grid(row=2, column=0, columnspan=3, sticky="w", pady=2)
        ttk.Radiobutton(pick_row, text="Pick location", variable=self.pos_mode_var, value="fixed").pack(side="left")
        self.pick_btn = self._flat_button(pick_row, "Pick", self.start_pick_location, width=6)
        self.pick_btn.pack(side="left", padx=6)
        ttk.Label(pick_row, text="X:").pack(side="left", padx=(10, 2))
        self.x_display = ttk.Entry(pick_row, width=5)
        self.x_display.insert(0, "0")
        self.x_display.pack(side="left")
        ttk.Label(pick_row, text="Y:").pack(side="left", padx=(6, 2))
        self.y_display = ttk.Entry(pick_row, width=5)
        self.y_display.insert(0, "0")
        self.y_display.pack(side="left")

        click_hold_section = self.make_section(click_body, "Hold Duration (Hold mode)")
        self.click_hold_vars = self.create_interval_row(click_hold_section, "Hold duration")

        click_hotkey_section = self.make_section(click_body, "Hotkey & Control")
        self.click_hotkey_entry, self.click_toggle_btn = self.create_hotkey_and_toggle_row(
            click_hotkey_section, default_hotkey="f6", toggle_command=self.toggle_clicker, action_label="Clicker",
            hotkey_which="click", running_attr="clicker_running")

    def build_press_tab(self, press_body):
        press_timing_section = self.make_section(press_body, "Timing")
        self.press_int_vars = self.create_interval_row(press_timing_section, "Press interval")

        key_section = self.make_section(press_body, "Key Options")
        key_frame = tk.Frame(key_section, bg=COLOR_CARD)
        key_frame.pack(fill="x")

        ttk.Label(key_frame, text="Key to press:").grid(row=0, column=0, sticky="w", padx=(0, 4), pady=2)
        self.press_key_var = tk.StringVar(value="space")
        self.press_key_combo = ttk.Combobox(key_frame, textvariable=self.press_key_var, values=ALL_KEYS, width=14)
        self.press_key_combo.grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(key_frame, text="Press type:").grid(row=0, column=2, sticky="w", padx=(16, 4), pady=2)
        self.press_type_var = tk.StringVar(value="Single")
        ttk.Combobox(key_frame, textvariable=self.press_type_var, values=["Single", "Double", "Triple"],
                     width=8, state="readonly").grid(row=0, column=3, sticky="w", pady=2)

        ttk.Label(key_frame, text="Action mode:").grid(row=0, column=4, sticky="w", padx=(16, 4), pady=2)
        self.press_action_mode_var = tk.StringVar(value="Click")
        ttk.Combobox(key_frame, textvariable=self.press_action_mode_var, values=["Click", "Hold"],
                     width=8, state="readonly").grid(row=0, column=5, sticky="w", pady=2)

        self.block_physical_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(key_frame, text="Block physical key", variable=self.block_physical_key_var,
                        style="Round.TCheckbutton").grid(
            row=1, column=0, columnspan=6, sticky="w", pady=(6, 0))

        self.pause_on_window_switch_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(key_frame, text="Pause on window switch", variable=self.pause_on_window_switch_var,
                        style="Round.TCheckbutton").grid(
            row=2, column=0, columnspan=6, sticky="w", pady=(4, 0))

        self.press_repeat_mode_var = tk.StringVar(value="infinite")
        ttk.Radiobutton(key_frame, text="Repeat until stopped", variable=self.press_repeat_mode_var,
                         value="infinite").grid(row=3, column=0, columnspan=6, sticky="w", pady=(6, 0))
        press_repeat_frame = tk.Frame(key_frame, bg=COLOR_CARD)
        press_repeat_frame.grid(row=4, column=0, columnspan=6, sticky="w", pady=2)
        ttk.Radiobutton(press_repeat_frame, text="Repeat press", variable=self.press_repeat_mode_var,
                         value="finite").pack(side="left")
        self.press_repeat_entry = ttk.Entry(press_repeat_frame, width=6)
        self.press_repeat_entry.insert(0, "100")
        self.press_repeat_entry.pack(side="left", padx=5)
        ttk.Label(press_repeat_frame, text="times").pack(side="left")

        self.press_max_speed_var = tk.BooleanVar(value=False)
        max_pps_row = tk.Frame(key_frame, bg=COLOR_CARD)
        max_pps_row.grid(row=5, column=0, columnspan=6, sticky="w", pady=(6, 0))
        ttk.Checkbutton(max_pps_row, text="Max PPS:",
                         variable=self.press_max_speed_var,
                         command=self.on_press_max_speed_toggle).pack(side="left")
        self.press_max_pps_entry = ttk.Entry(max_pps_row, width=6, justify="right", state="disabled")
        self.press_max_pps_entry.insert(0, "10")
        self.press_max_pps_entry.pack(side="left", padx=6)
        ttk.Label(max_pps_row, text="PPS").pack(side="left")
        self.press_pps_label = ttk.Label(max_pps_row, text="Current PPS: 0.0", style="Muted.TLabel")
        self.press_pps_label.pack(side="left", padx=(16, 0))

        press_mod_section = self.make_section(press_body, "Modifier Keys")
        press_mod_frame = tk.Frame(press_mod_section, bg=COLOR_CARD)
        press_mod_frame.pack(fill="x")

        self.press_mod_ctrl_var = tk.BooleanVar(value=False)
        self.press_mod_alt_var = tk.BooleanVar(value=False)
        self.press_mod_win_var = tk.BooleanVar(value=False)
        self.press_mod_shift_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(press_mod_frame, text="Ctrl", variable=self.press_mod_ctrl_var,
                        style="Round.TCheckbutton").pack(side="left", padx=(0, 20))
        ttk.Checkbutton(press_mod_frame, text="Alt", variable=self.press_mod_alt_var,
                        style="Round.TCheckbutton").pack(side="left", padx=(0, 20))
        ttk.Checkbutton(press_mod_frame, text="Win", variable=self.press_mod_win_var,
                        style="Round.TCheckbutton").pack(side="left", padx=(0, 20))
        ttk.Checkbutton(press_mod_frame, text="Shift", variable=self.press_mod_shift_var,
                        style="Round.TCheckbutton").pack(side="left")

        press_hold_section = self.make_section(press_body, "Hold Duration (Hold mode)")
        self.press_hold_vars = self.create_interval_row(press_hold_section, "Hold duration")

        press_hotkey_section = self.make_section(press_body, "Hotkey & Control")
        self.press_hotkey_entry, self.press_toggle_btn = self.create_hotkey_and_toggle_row(
            press_hotkey_section, default_hotkey="f7", toggle_command=self.toggle_presser, action_label="Presser",
            hotkey_which="press", running_attr="presser_running")

    def _build_recorder_ui(self, record_body, owner, show_recording=True, show_playback=True):
        target = owner if owner is not None else self

        def set_attr(name, value):
            setattr(target, name, value)

        def wrap(fn):
            return self._with_record_ctx(owner, fn)

        rec_section = (self.make_section(record_body, "Recording") if show_recording
                        else tk.Frame(record_body, bg=COLOR_CARD))

        rec_opts_row = tk.Frame(rec_section, bg=COLOR_CARD)
        rec_opts_row.pack(fill="x")
        record_moves_var = tk.BooleanVar(value=False)
        record_keys_var = tk.BooleanVar(value=True)
        set_attr('record_moves_var', record_moves_var)
        set_attr('record_keys_var', record_keys_var)
        ttk.Checkbutton(rec_opts_row, text="Record mouse movement",
                        variable=record_moves_var).grid(row=0, column=0, sticky="w", padx=(0, 16), pady=2)
        ttk.Checkbutton(rec_opts_row, text="Record keyboard",
                        variable=record_keys_var).grid(row=0, column=1, sticky="w", pady=2)

        move_rate_row = tk.Frame(rec_section, bg=COLOR_CARD)
        move_rate_row.pack(fill="x", pady=(4, 0))
        ttk.Label(move_rate_row, text="Record mouse position every (ms):").pack(side="left")
        record_move_interval_entry = ttk.Entry(move_rate_row, width=6, justify="center")
        record_move_interval_entry.insert(0, str(DEFAULT_MOVE_RECORD_INTERVAL_MS))
        record_move_interval_entry.pack(side="left", padx=(6, 0))
        set_attr('record_move_interval_entry', record_move_interval_entry)

        record_count_label = tk.Label(rec_section, text="Recorded events: 0", bg=COLOR_CARD,
                                       fg=COLOR_MUTED, font=("Segoe UI", 8))
        record_count_label.pack(anchor="w", pady=(8, 0))
        set_attr('record_count_label', record_count_label)

        record_which = self._record_hotkey_which(owner, "record")
        record_hotkey_entry, record_toggle_btn = self.create_hotkey_and_toggle_row(
            rec_section, default_hotkey=("f8" if owner is None else ""),
            toggle_command=wrap(self.toggle_recording), action_label="Recording",
            hotkey_which=record_which, running_attr='recording',
            running_attr_getter=lambda o=owner: self._record_running_attr_value(o, 'recording'))
        set_attr('record_hotkey_entry', record_hotkey_entry)
        set_attr('record_toggle_btn', record_toggle_btn)

        list_section = self.make_section(record_body, "Recorded Actions" if owner is None else "Actions")
        list_border = tk.Frame(list_section, bg=COLOR_BORDER)
        list_border.pack(fill="both", expand=True)
        list_row = tk.Frame(list_border, bg=COLOR_CARD)
        list_row.pack(fill="both", expand=True, padx=1, pady=1)

        list_scrollbar = ttk.Scrollbar(list_row, orient="vertical", style="Modern.Vertical.TScrollbar")
        record_tree = ttk.Treeview(list_row, columns=("stt", "time", "type", "detail"), show="headings",
                                    height=(8 if owner is None else 6), yscrollcommand=list_scrollbar.set,
                                    selectmode="browse", style="Record.Treeview")
        set_attr('record_tree', record_tree)
        record_tree.heading("stt", text="#", anchor="center")
        record_tree.heading("time", text="Time (s)", anchor="center")
        record_tree.heading("type", text="Type", anchor="center")
        record_tree.heading("detail", text="Detail", anchor="center")
        stt_w, time_w, type_w, detail_w = 50, 70, 100, 120
        record_tree.column("stt", width=stt_w, minwidth=36, anchor="center", stretch=False)
        record_tree.column("time", width=time_w, minwidth=60, anchor="center", stretch=False)
        record_tree.column("type", width=type_w, minwidth=60, anchor="center", stretch=False)
        record_tree.column("detail", width=detail_w, minwidth=80, anchor="center", stretch=False)
        list_scrollbar.config(command=record_tree.yview)
        record_tree.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        record_tree.bind("<Double-1>", lambda e: wrap(self._on_record_tree_double_click)(e))
        record_tree.bind("<Button-3>", lambda e: wrap(self._show_record_context_menu)(e))

        divider1 = tk.Frame(list_row, bg=COLOR_BORDER, width=1)
        divider2 = tk.Frame(list_row, bg=COLOR_BORDER, width=1)
        divider3 = tk.Frame(list_row, bg=COLOR_BORDER, width=1)
        divider1.place(in_=record_tree, x=stt_w, y=0, relheight=1)
        divider2.place(in_=record_tree, x=stt_w + time_w, y=0, relheight=1)
        divider3.place(in_=record_tree, x=stt_w + time_w + type_w, y=0, relheight=1)
        divider1.lift()
        divider2.lift()
        divider3.lift()

        last_width = {'val': -1}

        def _resize(event=None):
            total_width = record_tree.winfo_width()
            if total_width < 30 or total_width == last_width['val']:
                return
            last_width['val'] = total_width
            ratios = (stt_w / 340, time_w / 340, type_w / 340, detail_w / 340)
            w1 = int(total_width * ratios[0])
            w2 = int(total_width * ratios[1])
            w3 = int(total_width * ratios[2])
            w4 = max(0, total_width - w1 - w2 - w3)
            record_tree.column("stt", width=w1)
            record_tree.column("time", width=w2)
            record_tree.column("type", width=w3)
            record_tree.column("detail", width=w4)
            divider1.place(in_=record_tree, x=w1, y=0, relheight=1)
            divider2.place(in_=record_tree, x=w1 + w2, y=0, relheight=1)
            divider3.place(in_=record_tree, x=w1 + w2 + w3, y=0, relheight=1)
            divider1.lift()
            divider2.lift()
            divider3.lift()

        record_tree.bind("<Configure>", _resize, add="+")

        def _tree_mousewheel(event):
            record_tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def _tree_mousewheel_linux_up(event):
            record_tree.yview_scroll(-1, "units")
            return "break"

        def _tree_mousewheel_linux_down(event):
            record_tree.yview_scroll(1, "units")
            return "break"

        record_tree.bind("<MouseWheel>", _tree_mousewheel)
        record_tree.bind("<Button-4>", _tree_mousewheel_linux_up)
        record_tree.bind("<Button-5>", _tree_mousewheel_linux_down)

        actions_grid = tk.Frame(list_section, bg=COLOR_CARD)
        actions_grid.pack(fill="x", pady=(8, 0))
        for col in range(3):
            actions_grid.columnconfigure(col, weight=1, uniform=f"record_action_btn_{id(actions_grid)}")

        action_specs = (
            ("Add Action", wrap(self._add_new_event), 0, 0),
            ("Delete Action", wrap(self._delete_selected_event), 0, 1),
            ("Edit", wrap(self._edit_selected_event), 0, 2),
            ("Clear", wrap(self.clear_recorded_events), 1, 0),
            ("Download", wrap(self._download_recorded_events), 1, 1),
            ("Import", wrap(self._import_recorded_events), 1, 2),
        )
        for text, command, row, col in action_specs:
            btn = self._flat_button(actions_grid, text, command, width=1)
            btn.grid(row=row, column=col, sticky="ew",
                     padx=(0 if col == 0 else 6, 0), pady=(0 if row == 0 else 6, 0))

        play_section = (self.make_section(record_body, "Playback") if show_playback
                         else tk.Frame(record_body, bg=COLOR_CARD))

        playback_repeat_mode_var = tk.StringVar(value=("infinite" if owner is None else "finite"))
        set_attr('playback_repeat_mode_var', playback_repeat_mode_var)
        ttk.Radiobutton(play_section, text="Repeat until stopped", variable=playback_repeat_mode_var,
                         value="infinite").pack(anchor="w")
        play_repeat_row = tk.Frame(play_section, bg=COLOR_CARD)
        play_repeat_row.pack(fill="x", pady=2, anchor="w")
        ttk.Radiobutton(play_repeat_row, text="Repeat playback", variable=playback_repeat_mode_var,
                         value="finite").pack(side="left")
        playback_repeat_entry = ttk.Entry(play_repeat_row, width=6)
        playback_repeat_entry.insert(0, "1")
        playback_repeat_entry.pack(side="left", padx=5)
        set_attr('playback_repeat_entry', playback_repeat_entry)
        ttk.Label(play_repeat_row, text="times").pack(side="left")

        speed_row = tk.Frame(play_section, bg=COLOR_CARD)
        speed_row.pack(fill="x", pady=(8, 4), anchor="w")
        ttk.Label(speed_row, text="Playback speed (x):").pack(side="left")
        playback_speed_entry = ttk.Entry(speed_row, width=6, justify="right")
        playback_speed_entry.insert(0, "1.0")
        playback_speed_entry.pack(side="left", padx=6)
        set_attr('playback_speed_entry', playback_speed_entry)

        playback_which = self._record_hotkey_which(owner, "playback")
        playback_hotkey_entry, playback_toggle_btn = self.create_hotkey_and_toggle_row(
            play_section, default_hotkey=("f9" if owner is None else ""),
            toggle_command=wrap(self.toggle_playback), action_label="Playback",
            hotkey_which=playback_which, running_attr='playing',
            running_attr_getter=lambda o=owner: self._record_running_attr_value(o, 'playing'))
        set_attr('playback_hotkey_entry', playback_hotkey_entry)
        set_attr('playback_toggle_btn', playback_toggle_btn)

    def build_record_tab(self, record_body):
        self._build_recorder_ui(record_body, owner=None)

    def build_pixel_watch_tab(self, body):
        self._pixel_watch_tab_body = body
        bar = tk.Frame(body, bg=COLOR_CARD)
        bar.pack(fill="x", pady=(0, 10))
        self._flat_button(bar, "+ Add Watcher", self._add_pixel_watcher, width=14).pack(side="left")
        self._flat_button(bar, "- Delete Watcher", self._prompt_delete_pixel_watcher,
                           width=14).pack(side="left", padx=(6, 0))

        list_border = tk.Frame(body, bg=COLOR_BORDER)
        list_border.pack(fill="both", expand=True)
        list_canvas, list_scrollbar, self.pixel_watch_list = self._make_scroll_area(
            list_border, COLOR_BG, height=320)
        list_canvas.pack(fill="both", expand=True, padx=1, pady=1)

        for watcher in self.pixel_watchers:
            self._build_pixel_watcher_card(watcher)
            if watcher.window is None:
                self._build_pixel_watcher_window(watcher)

    def _add_pixel_watcher(self, restore=None):
        watcher = PixelWatcher(self._pixel_watcher_next_id,
                                title=(restore or {}).get('title') or f"Watcher {len(self.pixel_watchers) + 1}")
        self._pixel_watcher_next_id += 1
        self.pixel_watchers.append(watcher)
        self._build_pixel_watcher_card(watcher)
        self._build_pixel_watcher_window(watcher)
        if restore:
            self._apply_pixel_watcher_dict(watcher, restore)
        return watcher

    def _build_pixel_watcher_card(self, watcher):
        card_border = tk.Frame(self.pixel_watch_list, bg=COLOR_SECTION_BORDER)
        card_border.pack(fill="x", pady=(0, 8))
        card = tk.Frame(card_border, bg=COLOR_CARD, padx=10, pady=8)
        card.pack(fill="both", expand=True, padx=1, pady=1)
        watcher.card = card_border

        top_row = tk.Frame(card, bg=COLOR_CARD)
        top_row.pack(fill="x")
        title_label = tk.Label(top_row, text=watcher.title, bg=COLOR_CARD, fg=COLOR_TEXT,
                                font=("Segoe UI", 9, "bold"), cursor="hand2")
        title_label.pack(side="left")
        title_label.bind("<Double-Button-1>", lambda e, w=watcher: self._rename_pixel_watcher(w))
        watcher.card_title_label = title_label

        btn_row = tk.Frame(card, bg=COLOR_CARD)
        btn_row.pack(fill="x", pady=(8, 0))
        self._flat_button(btn_row, "Open", lambda w=watcher: self._open_pixel_watcher_window(w),
                           width=6).pack(side="left")
        self._flat_button(btn_row, "Download", lambda w=watcher: self._download_pixel_watcher(w),
                           width=8).pack(side="left", padx=(4, 0))
        self._flat_button(btn_row, "Import", lambda w=watcher: self._import_pixel_watcher(w),
                           width=6).pack(side="left", padx=(4, 0))
        card_toggle_btn = self._flat_button(
            btn_row, ("Stop Watching" if watcher.running else "Start Watching"),
            lambda w=watcher: self.toggle_pixel_watch(w), width=12)
        card_toggle_btn.pack(side="left", padx=(4, 0))
        watcher.card_toggle_btn = card_toggle_btn
        self._set_toggle_running_style(card_toggle_btn, watcher.running)
        self._flat_button(btn_row, "Delete", lambda w=watcher: self._delete_pixel_watcher(w),
                           width=6).pack(side="right")

    def _open_pixel_watcher_window(self, watcher):
        watcher.window.deiconify()
        watcher.window.lift()
        watcher.window.focus_force()

    def _rename_pixel_watcher(self, watcher):
        new_name = self._prompt_profile_name("Rename Watcher", default=watcher.title)
        if not new_name:
            return
        watcher.title = new_name
        watcher.card_title_label.config(text=new_name)
        if watcher.window is not None:
            watcher.window.title(new_name)

    def _prompt_delete_pixel_watcher(self):
        if not self.pixel_watchers:
            messagebox.showinfo("Delete Watcher", "No watchers to delete.", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Watchers")
        dialog.configure(bg=COLOR_CARD)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.withdraw()

        ttk.Label(dialog, text="Select watchers to delete:").pack(anchor="w", padx=12, pady=(12, 6))

        list_border = tk.Frame(dialog, bg=COLOR_BORDER)
        list_border.pack(fill="both", expand=True, padx=12)
        list_canvas, list_scrollbar, list_inner = self._make_scroll_area(
            list_border, COLOR_CARD, height=min(220, 28 * len(self.pixel_watchers) + 10))
        list_canvas.pack(fill="both", expand=True, padx=1, pady=1)

        check_vars = []
        for watcher in self.pixel_watchers:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(list_inner, text=watcher.title, variable=var,
                             style="Round.TCheckbutton").pack(anchor="w", padx=8, pady=3)
            check_vars.append((watcher, var))

        select_row = tk.Frame(dialog, bg=COLOR_CARD)
        select_row.pack(fill="x", padx=12, pady=(8, 0))

        def select_all():
            for _, var in check_vars:
                var.set(True)

        def select_none():
            for _, var in check_vars:
                var.set(False)

        self._flat_button(select_row, "Select All", select_all, width=10).pack(side="left")
        self._flat_button(select_row, "Select None", select_none, width=10).pack(side="left", padx=(6, 0))

        btn_row = tk.Frame(dialog, bg=COLOR_CARD)
        btn_row.pack(fill="x", padx=12, pady=(10, 12))

        outcome = {'ok': False}

        def on_delete():
            outcome['ok'] = True
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        self._flat_button(btn_row, "Delete Selected", on_delete, width=14).pack(side="left")
        self._flat_button(btn_row, "Cancel", on_cancel, width=10).pack(side="left", padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        self._center_dialog_over_widget(dialog, self._pixel_watch_tab_body)
        dialog.deiconify()
        dialog.grab_set()
        self.root.wait_window(dialog)

        if not outcome['ok']:
            return
        selected = [w for w, var in check_vars if var.get()]
        if not selected:
            return
        if any(w is self._active_record_owner and (self.recording or self.playing) for w in selected):
            messagebox.showinfo("Delete Watcher",
                                 "One of the selected watchers is recording or playing back - stop it first.",
                                 parent=self.root)
            return
        names = ", ".join(f'"{w.title}"' for w in selected)
        if not messagebox.askyesno("Delete Watchers",
                                    f"Delete {len(selected)} watcher(s)?\n{names}", parent=self.root):
            return
        for watcher in selected:
            self._delete_pixel_watcher(watcher, confirm=False)

    def _delete_pixel_watcher(self, watcher, confirm=True):
        if watcher is self._active_record_owner and (self.recording or self.playing):
            messagebox.showinfo("Delete Watcher",
                                 "This watcher is recording or playing back - stop it first.",
                                 parent=self.root)
            return
        if confirm and not messagebox.askyesno("Delete Watcher", f"Delete \"{watcher.title}\"?", parent=self.root):
            return
        if watcher.running and watcher.stop_event is not None:
            watcher.running = False
            watcher.stop_event.set()
        if watcher is self._active_record_owner:
            self._use_record_ctx(None)
        for which in (watcher.hotkey_which, self._record_hotkey_which(watcher, "record"),
                      self._record_hotkey_which(watcher, "playback")):
            spec = self.hotkey_specs.pop(which, None)
            if spec is not None:
                handle = spec.get('registered_handle')
                if handle is not None:
                    try:
                        keyboard.remove_hotkey(handle)
                    except Exception:
                        pass
        if watcher.window is not None:
            watcher.window.destroy()
        watcher.card.destroy()
        self.pixel_watchers.remove(watcher)

    def _build_pixel_watcher_window(self, watcher):
        window = tk.Toplevel(self.root)
        window.title(watcher.title)
        window.configure(bg=COLOR_CARD)
        window.protocol("WM_DELETE_WINDOW", window.withdraw)
        window.withdraw()
        watcher.window = window

        canvas, scrollbar, inner = self._make_scroll_area(window, COLOR_CARD)
        canvas.pack(fill="both", expand=True)

        body = tk.Frame(inner, bg=COLOR_CARD, padx=12, pady=12)
        body.pack(fill="both", expand=True)
        watcher.frame = body
        self.build_single_pixel_watcher_tab(body, watcher)

        self.root.update_idletasks()
        tab_width = self.content_area.winfo_width() or self.root.winfo_width()
        content_height = body.winfo_reqheight()
        screen_h = self.root.winfo_screenheight()
        max_height = screen_h - 120
        target_height = min(content_height, max_height)
        window.geometry(f"{max(tab_width, 1)}x{max(target_height, 1)}")
        window.resizable(False, False)

    def build_single_pixel_watcher_tab(self, body, watcher):
        loc_section = self.make_section(body, "Pixel Location")

        pick_row = tk.Frame(loc_section, bg=COLOR_CARD)
        pick_row.pack(fill="x")
        watcher.pick_btn = self._flat_button(
            pick_row, "Pick", lambda w=watcher: self.start_pick_location(
                w.x_entry, w.y_entry, on_done=lambda w=w: self._sample_pixel_now(w)), width=6)
        watcher.pick_btn.pack(side="left")
        ttk.Label(pick_row, text="X:").pack(side="left", padx=(10, 2))
        watcher.x_entry = ttk.Entry(pick_row, width=5)
        watcher.x_entry.insert(0, "0")
        watcher.x_entry.pack(side="left")
        ttk.Label(pick_row, text="Y:").pack(side="left", padx=(6, 2))
        watcher.y_entry = ttk.Entry(pick_row, width=5)
        watcher.y_entry.insert(0, "0")
        watcher.y_entry.pack(side="left")

        preview_row = tk.Frame(loc_section, bg=COLOR_CARD)
        preview_row.pack(fill="x", pady=(8, 0))
        ttk.Label(preview_row, text="Current color:", style="Muted.TLabel").pack(side="left")
        watcher.preview_swatch = tk.Canvas(preview_row, width=22, height=22, bg="#000000",
                                            highlightthickness=1, highlightbackground=COLOR_SECTION_BORDER)
        watcher.preview_swatch.pack(side="left", padx=(8, 4))
        watcher.preview_hex_entry = ttk.Entry(preview_row, width=10)
        watcher.preview_hex_entry.pack(side="left")

        preview_rgb_row = tk.Frame(loc_section, bg=COLOR_CARD)
        preview_rgb_row.pack(fill="x", pady=(4, 0))
        watcher.preview_r_entry, watcher.preview_g_entry, watcher.preview_b_entry = \
            self._make_rgb_entries(preview_rgb_row, 0, 0, 0)

        watcher.preview_hex_entry.bind(
            "<KeyRelease>", lambda e, w=watcher: self._sync_rgb_from_hex(
                w.preview_hex_entry, w.preview_r_entry, w.preview_g_entry, w.preview_b_entry, w.preview_swatch))
        watcher.preview_hex_entry.bind(
            "<FocusOut>", lambda e, w=watcher: self._sync_rgb_from_hex(
                w.preview_hex_entry, w.preview_r_entry, w.preview_g_entry, w.preview_b_entry, w.preview_swatch))
        for entry in (watcher.preview_r_entry, watcher.preview_g_entry, watcher.preview_b_entry):
            entry.bind("<KeyRelease>", lambda e, w=watcher: self._sync_hex_from_rgb(
                w.preview_r_entry, w.preview_g_entry, w.preview_b_entry, w.preview_hex_entry, w.preview_swatch))
            entry.bind("<FocusOut>", lambda e, w=watcher: self._sync_hex_from_rgb(
                w.preview_r_entry, w.preview_g_entry, w.preview_b_entry, w.preview_hex_entry, w.preview_swatch))

        cond_section = self.make_section(body, "Trigger Condition")
        watcher.mode_var = tk.StringVar(value="any")
        ttk.Radiobutton(cond_section, text="Trigger when the color changes to ANY new color",
                         variable=watcher.mode_var, value="any",
                         command=lambda w=watcher: self._on_pixel_mode_changed(w)).pack(anchor="w")
        ttk.Radiobutton(cond_section, text="Trigger when the color changes to a specific color",
                         variable=watcher.mode_var, value="specific",
                         command=lambda w=watcher: self._on_pixel_mode_changed(w)).pack(anchor="w", pady=(2, 0))

        watcher.target_frame = tk.Frame(cond_section, bg=COLOR_CARD)
        watcher.target_frame.pack(fill="x", pady=(6, 0), padx=(20, 0))

        target_row = tk.Frame(watcher.target_frame, bg=COLOR_CARD)
        target_row.pack(fill="x")
        ttk.Label(target_row, text="Target color (hex):").pack(side="left")
        watcher.target_swatch = tk.Canvas(target_row, width=22, height=22, bg="#ff0000",
                                           highlightthickness=1, highlightbackground=COLOR_SECTION_BORDER)
        watcher.target_swatch.pack(side="left", padx=(8, 4))
        watcher.target_hex_entry = ttk.Entry(target_row, width=10)
        watcher.target_hex_entry.insert(0, "#ff0000")
        watcher.target_hex_entry.pack(side="left")

        target_rgb_row = tk.Frame(watcher.target_frame, bg=COLOR_CARD)
        target_rgb_row.pack(fill="x", pady=(4, 0))
        watcher.target_r_entry, watcher.target_g_entry, watcher.target_b_entry = \
            self._make_rgb_entries(target_rgb_row, 255, 0, 0)

        watcher.target_hex_entry.bind(
            "<KeyRelease>", lambda e, w=watcher: self._sync_rgb_from_hex(
                w.target_hex_entry, w.target_r_entry, w.target_g_entry, w.target_b_entry, w.target_swatch))
        watcher.target_hex_entry.bind(
            "<FocusOut>", lambda e, w=watcher: self._sync_rgb_from_hex(
                w.target_hex_entry, w.target_r_entry, w.target_g_entry, w.target_b_entry, w.target_swatch))
        for entry in (watcher.target_r_entry, watcher.target_g_entry, watcher.target_b_entry):
            entry.bind("<KeyRelease>", lambda e, w=watcher: self._sync_hex_from_rgb(
                w.target_r_entry, w.target_g_entry, w.target_b_entry, w.target_hex_entry, w.target_swatch))
            entry.bind("<FocusOut>", lambda e, w=watcher: self._sync_hex_from_rgb(
                w.target_r_entry, w.target_g_entry, w.target_b_entry, w.target_hex_entry, w.target_swatch))

        tol_row = tk.Frame(watcher.target_frame, bg=COLOR_CARD)
        tol_row.pack(fill="x", pady=(6, 0))
        ttk.Label(tol_row, text="Tolerance (per channel, 0-255):").pack(side="left")
        watcher.tolerance_entry = ttk.Entry(tol_row, width=5)
        watcher.tolerance_entry.insert(0, "20")
        watcher.tolerance_entry.pack(side="left", padx=6)

        self._on_pixel_mode_changed(watcher)

        timing_section = self.make_section(body, "Check Timing")
        interval_row = tk.Frame(timing_section, bg=COLOR_CARD)
        interval_row.pack(fill="x")
        ttk.Label(interval_row, text="Check interval (ms):").pack(side="left")
        watcher.interval_entry = ttk.Entry(interval_row, width=6)
        watcher.interval_entry.insert(0, "200")
        watcher.interval_entry.pack(side="left", padx=6)

        cooldown_row = tk.Frame(timing_section, bg=COLOR_CARD)
        cooldown_row.pack(fill="x", pady=(6, 0))
        ttk.Label(cooldown_row, text="Cooldown after trigger (s):").pack(side="left")
        watcher.cooldown_entry = ttk.Entry(cooldown_row, width=6)
        watcher.cooldown_entry.insert(0, "2.0")
        watcher.cooldown_entry.pack(side="left", padx=6)

        watcher.stop_after_trigger_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(timing_section, text="Stop watching after the first trigger",
                         variable=watcher.stop_after_trigger_var,
                         style="Round.TCheckbutton").pack(anchor="w", pady=(6, 0))

        self.build_watcher_actions_section(body, watcher)

    def build_watcher_actions_section(self, body, watcher):
        self._build_recorder_ui(body, owner=watcher, show_recording=False, show_playback=False)

    def _on_pixel_mode_changed(self, watcher):
        if watcher.mode_var.get() == "specific":
            watcher.target_frame.pack(fill="x", pady=(6, 0), padx=(20, 0))
        else:
            watcher.target_frame.pack_forget()

    def _get_pixel_color(self, x, y):
        if not hasattr(ctypes, "windll"):
            return None
        try:
            hdc = ctypes.windll.user32.GetDC(None)
            if not hdc:
                return None
            try:
                colorref = ctypes.windll.gdi32.GetPixel(hdc, int(x), int(y))
            finally:
                ctypes.windll.user32.ReleaseDC(None, hdc)
            if colorref == 0xFFFFFFFF:
                return None
            r = colorref & 0xFF
            g = (colorref >> 8) & 0xFF
            b = (colorref >> 16) & 0xFF
            return (r, g, b)
        except Exception:
            return None

    def _color_matches(self, color, target, tolerance):
        if color is None:
            return False
        return all(abs(c - t) <= tolerance for c, t in zip(color, target))

    def _parse_hex_color(self, text):
        if not text:
            return None
        t = text.strip().lstrip('#')
        if len(t) == 3:
            t = ''.join(c * 2 for c in t)
        if len(t) != 6:
            return None
        try:
            r = int(t[0:2], 16)
            g = int(t[2:4], 16)
            b = int(t[4:6], 16)
            return (r, g, b)
        except ValueError:
            return None

    def _make_rgb_entries(self, parent, r_default, g_default, b_default):
        ttk.Label(parent, text="R:").pack(side="left")
        r_entry = ttk.Entry(parent, width=4)
        r_entry.insert(0, str(r_default))
        r_entry.pack(side="left", padx=(2, 8))
        ttk.Label(parent, text="G:").pack(side="left")
        g_entry = ttk.Entry(parent, width=4)
        g_entry.insert(0, str(g_default))
        g_entry.pack(side="left", padx=(2, 8))
        ttk.Label(parent, text="B:").pack(side="left")
        b_entry = ttk.Entry(parent, width=4)
        b_entry.insert(0, str(b_default))
        b_entry.pack(side="left")
        return r_entry, g_entry, b_entry

    def _sync_rgb_from_hex(self, hex_entry, r_entry, g_entry, b_entry, canvas):
        rgb = self._parse_hex_color(hex_entry.get())
        if rgb is None:
            return
        r, g, b = rgb
        canvas.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        self._set_entry_text(r_entry, r)
        self._set_entry_text(g_entry, g)
        self._set_entry_text(b_entry, b)

    def _sync_hex_from_rgb(self, r_entry, g_entry, b_entry, hex_entry, canvas):
        try:
            r = max(0, min(255, int(r_entry.get() or 0)))
            g = max(0, min(255, int(g_entry.get() or 0)))
            b = max(0, min(255, int(b_entry.get() or 0)))
        except ValueError:
            return
        hexcode = f"#{r:02x}{g:02x}{b:02x}"
        self._set_entry_text(hex_entry, hexcode)
        canvas.config(bg=hexcode)

    def _update_pixel_preview(self, watcher, color):
        try:
            if color is None:
                watcher.preview_swatch.config(bg=COLOR_CARD)
                self._set_entry_text(watcher.preview_hex_entry, "")
                return
            r, g, b = color
            hexcode = f"#{r:02x}{g:02x}{b:02x}"
            watcher.preview_swatch.config(bg=hexcode)
            self._set_entry_text(watcher.preview_hex_entry, hexcode)
            self._set_entry_text(watcher.preview_r_entry, r)
            self._set_entry_text(watcher.preview_g_entry, g)
            self._set_entry_text(watcher.preview_b_entry, b)
        except Exception:
            pass

    def _sample_pixel_now(self, watcher):
        try:
            x = int(watcher.x_entry.get())
            y = int(watcher.y_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Position", "Please enter valid X and Y coordinates.", parent=self.root)
            return
        color = self._get_pixel_color(x, y)
        self._update_pixel_preview(watcher, color)

    def build_profile_tab(self, profile_body):
        info_section = self.make_section(profile_body, "Active Profile")
        self.active_profile_label = tk.Label(
            info_section, text="Active: -", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 10, "bold"))
        self.active_profile_label.pack(anchor="w")

        desc_label = ttk.Label(
            info_section,
            text="Saves settings from the other 3 tabs. Select a profile and click "
                 "Apply to use it, or New to save the current settings as a profile.",
            style="Muted.TLabel", justify="left")
        desc_label.pack(anchor="w", fill="x", pady=(4, 0))
        desc_label.config(wraplength=440)

        self.auto_save_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            info_section, text="Auto save changes to the active profile",
            variable=self.auto_save_var, command=self._on_auto_save_toggle).pack(anchor="w", pady=(8, 0))

        list_section = self.make_section(profile_body, "Profiles")
        list_border = tk.Frame(list_section, bg=COLOR_BORDER)
        list_border.pack(fill="both", expand=True)
        list_row = tk.Frame(list_border, bg=COLOR_CARD)
        list_row.pack(fill="both", expand=True, padx=1, pady=1)

        list_scrollbar = ttk.Scrollbar(list_row, orient="vertical", style="Modern.Vertical.TScrollbar")
        self.profile_tree = ttk.Treeview(
            list_row, columns=("name",), show="headings", height=8,
            yscrollcommand=list_scrollbar.set, selectmode="browse", style="Record.Treeview")
        self.profile_tree.heading("name", text="Profile Name", anchor="w")
        self.profile_tree.column("name", anchor="w", stretch=True)
        list_scrollbar.config(command=self.profile_tree.yview)
        self.profile_tree.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        self.profile_tree.bind("<Double-1>", lambda e: self.apply_selected_profile())

        def _profile_button_row(parent, specs):
            row = tk.Frame(parent, bg=COLOR_CARD)
            for col in range(3):
                row.columnconfigure(col, weight=1, uniform="profile_btn_col")
            for col, (text, cmd) in enumerate(specs):
                pad = (0, 4) if col == 0 else ((4, 0) if col == 2 else 4)
                self._flat_button(row, text, cmd, width=9).grid(
                    row=0, column=col, sticky="ew", padx=pad)
            return row

        _profile_button_row(profile_body, [
            ("New", self.new_profile), ("Save", self.save_current_profile), ("Apply", self.apply_selected_profile),
        ]).pack(fill="x", pady=(8, 0))

        _profile_button_row(profile_body, [
            ("Rename", self.rename_selected_profile), ("Edit", self.edit_selected_profile),
            ("Delete", self.delete_selected_profile),
        ]).pack(fill="x", pady=(6, 0))

        _profile_button_row(profile_body, [
            ("Clear", self.clear_profiles), ("Download", self.download_profiles), ("Import", self.import_profiles),
        ]).pack(fill="x", pady=(6, 0))

    def refresh_profile_list(self):
        if not hasattr(self, "profile_tree"):
            return
        self.profile_tree.delete(*self.profile_tree.get_children())
        to_select = None
        for name in self.profiles.keys():
            label = f"{name}  (active)" if name == self.active_profile_name else name
            iid = self.profile_tree.insert("", "end", values=(label,))
            self.profile_tree.item(iid, tags=(name,))
            if name == self.active_profile_name:
                to_select = iid
        if to_select:
            self.profile_tree.selection_set(to_select)
            self.profile_tree.see(to_select)
        self.active_profile_label.config(text=f"Active: {self.active_profile_name or '-'}")

    def _selected_profile_name(self):
        sel = self.profile_tree.selection()
        if not sel:
            return None
        tags = self.profile_tree.item(sel[0], "tags")
        return tags[0] if tags else None

    def _require_selected_profile(self):
        name = self._selected_profile_name()
        if not name:
            messagebox.showinfo("No profile selected", "Select a profile from the list first.", parent=self.root)
        return name

    def _prompt_profile_name(self, title, default=""):
        result = self._prompt_fields(title, [
            {'key': 'name', 'label': 'Name', 'type': 'entry', 'default': default},
        ], over_widget=self._profile_tab)
        return result['name'].strip() if result else None

    def new_profile(self):
        name = self._prompt_profile_name("New Profile")
        if not name:
            return
        if name in self.profiles and not messagebox.askyesno(
                "Already exists", f"Profile '{name}' already exists. Overwrite?", parent=self.root):
            return
        self.profiles[name] = self.get_settings_dict()
        self.active_profile_name = name
        self.save_profiles_store()
        self.refresh_profile_list()

    def save_current_profile(self):
        name = self._selected_profile_name() or self.active_profile_name
        if not name:
            messagebox.showinfo("No profile selected", "Select a profile, or click New to create one.",
                                 parent=self.root)
            return
        self.profiles[name] = self.get_settings_dict()
        self.active_profile_name = name
        self.save_profiles_store()
        self.refresh_profile_list()

    def apply_selected_profile(self):
        name = self._require_selected_profile()
        if not name:
            return
        if name != self.active_profile_name:
            self._autosave_active_profile()
        self.apply_settings_dict(self.profiles[name])
        self._reregister_all_hotkeys()
        self.active_profile_name = name
        self.save_profiles_store()
        self.refresh_profile_list()

    def rename_selected_profile(self):
        name = self._require_selected_profile()
        if not name:
            return
        new_name = self._prompt_profile_name("Rename Profile", default=name)
        if not new_name or new_name == name:
            return
        if new_name in self.profiles:
            messagebox.showwarning("Already exists", f"Profile '{new_name}' already exists.", parent=self.root)
            return
        self.profiles[new_name] = self.profiles.pop(name)
        if self.active_profile_name == name:
            self.active_profile_name = new_name
        self.save_profiles_store()
        self.refresh_profile_list()

    def edit_selected_profile(self):
        name = self._require_selected_profile()
        if not name:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Profile - {name}")
        dialog.configure(bg=COLOR_CARD)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.withdraw()

        ttk.Label(dialog, text="Raw settings (JSON) - edit carefully.", style="Muted.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 4))

        text_frame = tk.Frame(dialog, bg=COLOR_CARD)
        text_frame.grid(row=1, column=0, columnspan=2, padx=8, pady=(0, 4), sticky="nsew")
        text_scroll = ttk.Scrollbar(text_frame, orient="vertical", style="Modern.Vertical.TScrollbar")
        text_widget = tk.Text(text_frame, width=64, height=22, wrap="none",
                               yscrollcommand=text_scroll.set, font=("Consolas", 9))
        text_scroll.config(command=text_widget.yview)
        text_widget.pack(side="left", fill="both", expand=True)
        text_scroll.pack(side="right", fill="y")
        text_widget.insert("1.0", json.dumps(self.profiles.get(name, {}), indent=2, ensure_ascii=False))

        outcome = {'ok': False, 'data': None}

        def on_ok():
            try:
                parsed = json.loads(text_widget.get("1.0", "end-1c"))
            except Exception as exc:
                messagebox.showerror("Invalid JSON", f"Could not parse JSON:\n{exc}", parent=dialog)
                return
            if not isinstance(parsed, dict):
                messagebox.showerror("Invalid JSON", "Top-level value must be an object.", parent=dialog)
                return
            outcome['ok'] = True
            outcome['data'] = parsed
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        self._add_save_cancel_buttons(dialog, 2, on_ok, on_cancel)
        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        self._position_dialog_over_widget(dialog, self._profile_tab)
        dialog.deiconify()
        dialog.grab_set()
        self.root.wait_window(dialog)

        if not outcome['ok']:
            return
        self.profiles[name] = outcome['data']
        if name == self.active_profile_name:
            self.apply_settings_dict(self.profiles[name])
            self._reregister_all_hotkeys()
        self.save_profiles_store()
        self.refresh_profile_list()

    def delete_selected_profile(self):
        name = self._require_selected_profile()
        if not name:
            return
        if len(self.profiles) <= 1:
            messagebox.showwarning("Can't delete", "At least one profile must remain.", parent=self.root)
            return
        if not messagebox.askyesno("Delete profile", f"Delete '{name}'? This can't be undone.", parent=self.root):
            return
        del self.profiles[name]
        if self.active_profile_name == name:
            self.active_profile_name = next(iter(self.profiles))
            self.apply_settings_dict(self.profiles[self.active_profile_name])
            self._reregister_all_hotkeys()
        self.save_profiles_store()
        self.refresh_profile_list()

    def _autosave_active_profile(self):
        if not self.auto_save_var.get() or not self.active_profile_name:
            return
        self.profiles[self.active_profile_name] = self.get_settings_dict()
        self.save_profiles_store()

    def _on_auto_save_toggle(self):
        self.save_profiles_store()

    def clear_profiles(self):
        if not messagebox.askyesno(
                "Clear profiles", "Remove all profiles except the current settings as 'Default'?",
                parent=self.root):
            return
        self.profiles = {'Default': self.get_settings_dict()}
        self.active_profile_name = 'Default'
        self.save_profiles_store()
        self.refresh_profile_list()

    def download_profiles(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, title="Download Profiles", defaultextension=".json",
            filetypes=[("JSON file", "*.json"), ("All files", "*.*")],
            initialfile="4FAutoClicker_profiles.json")
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'version': 1, 'active': self.active_profile_name, 'profiles': self.profiles},
                           f, indent=2)
        except Exception as exc:
            messagebox.showerror("Download failed", f"Could not save the file:\n{exc}", parent=self.root)
            return
        messagebox.showinfo("Download", "Profiles saved successfully.", parent=self.root)

    def import_profiles(self):
        path = filedialog.askopenfilename(
            parent=self.root, title="Import Profiles", filetypes=[("JSON file", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as exc:
            messagebox.showerror("Import failed", f"Could not read the file:\n{exc}", parent=self.root)
            return

        imported = data.get('profiles') if isinstance(data, dict) else None
        if not isinstance(imported, dict) or not imported:
            messagebox.showerror("Import failed", "This file doesn't contain valid profiles.", parent=self.root)
            return

        replace = messagebox.askyesno(
            "Import", f"Found {len(imported)} profile(s).\n\nYes = replace all\nNo = merge with current",
            parent=self.root)
        self.profiles = imported if replace else {**self.profiles, **imported}
        active = data.get('active')
        self.active_profile_name = active if active in self.profiles else next(iter(self.profiles))
        self.apply_settings_dict(self.profiles[self.active_profile_name])
        self._reregister_all_hotkeys()
        self.save_profiles_store()
        self.refresh_profile_list()

    def create_interval_row(self, parent, title):
        frame = tk.Frame(parent, bg=COLOR_CARD)
        frame.pack(fill="x", pady=(0, 4))

        ttk.Label(frame, text=title + ":", font=("Segoe UI", 9)).grid(
            row=0, column=0, columnspan=8, sticky="w", pady=(0, 4))

        ttk.Label(frame, text="Hours").grid(row=1, column=0, padx=2)
        ttk.Label(frame, text="Minutes").grid(row=1, column=2, padx=2)
        ttk.Label(frame, text="Seconds").grid(row=1, column=4, padx=2)
        ttk.Label(frame, text="Milliseconds").grid(row=1, column=6, padx=2)

        entries = {}
        for key, col, width, default in (('h', 0, 5, "0"), ('m', 2, 5, "0"),
                                          ('s', 4, 5, "0"), ('ms', 6, 6, "100")):
            ent = ttk.Entry(frame, width=width, justify="right")
            ent.insert(0, default)
            ent.grid(row=2, column=col, padx=2)
            entries[key] = ent

        rand_var = tk.BooleanVar(value=False)
        rand_chk = ttk.Checkbutton(frame, text="Random interval +/-", variable=rand_var)
        rand_chk.grid(row=3, column=0, columnspan=4, sticky="w", pady=(6, 0))

        rand_ent = ttk.Entry(frame, width=6, justify="right")
        rand_ent.insert(0, "20")
        rand_ent.grid(row=3, column=4, padx=2, pady=(6, 0))
        ttk.Label(frame, text="ms").grid(row=3, column=5, sticky="w", pady=(6, 0))

        return {'h': entries['h'], 'm': entries['m'], 's': entries['s'], 'ms': entries['ms'],
                'rand_var': rand_var, 'rand_ms': rand_ent, 'rand_chk': rand_chk}

    def on_click_max_speed_toggle(self):
        state = "normal" if self.click_max_speed_var.get() else "disabled"
        try:
            self.click_max_cps_entry.configure(state=state)
        except Exception:
            pass

    def on_press_max_speed_toggle(self):
        state = "normal" if self.press_max_speed_var.get() else "disabled"
        try:
            self.press_max_pps_entry.configure(state=state)
        except Exception:
            pass

    def update_rate_labels(self):
        click_running = getattr(self, "clicker_running", False)
        press_running = getattr(self, "presser_running", False)

        click_text = f"Current CPS: {self.click_rate_counter.rate():.1f}" if click_running else "Current CPS: 0.0"
        if click_text != self._last_click_cps_text:
            try:
                self.click_cps_label.config(text=click_text)
                self._last_click_cps_text = click_text
            except Exception:
                pass

        press_text = f"Current PPS: {self.press_rate_counter.rate():.1f}" if press_running else "Current PPS: 0.0"
        if press_text != self._last_press_pps_text:
            try:
                self.press_pps_label.config(text=press_text)
                self._last_press_pps_text = press_text
            except Exception:
                pass

        next_delay = 150 if (click_running or press_running) else 1000
        self.root.after(next_delay, self.update_rate_labels)

    def _on_global_click(self, event):
        try:
            cls = event.widget.winfo_class()
        except Exception:
            return
        if cls in BACKGROUND_WIDGET_CLASSES:
            try:
                self.root.focus_set()
            except Exception:
                pass

    def _fire_clicks(self, btn_type, clicks, stop_event=None):
        for i in range(clicks):
            mouse.click(button=btn_type)
            if i < clicks - 1:
                if stop_event is not None:
                    if stop_event.wait(MULTI_CLICK_GAP_S):
                        break
                else:
                    time.sleep(MULTI_CLICK_GAP_S)

    def _fire_presses(self, send_fn, presses, stop_event=None):
        for i in range(presses):
            send_fn()
            if i < presses - 1:
                if stop_event is not None:
                    if stop_event.wait(MULTI_CLICK_GAP_S):
                        break
                else:
                    time.sleep(MULTI_CLICK_GAP_S)

    def _safe_ui_after(self, callback):
        try:
            if self.root.winfo_exists():
                self.root.after(0, callback)
        except Exception:
            pass

    def _get_foreground_hwnd(self):
        if not hasattr(ctypes, "windll"):
            return None
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            return hwnd or None
        except Exception:
            return None

    def _get_own_hwnd(self):
        if not hasattr(ctypes, "windll"):
            return None
        try:
            GA_ROOT = 2
            child_hwnd = self.root.winfo_id()
            root_hwnd = ctypes.windll.user32.GetAncestor(child_hwnd, GA_ROOT)
            return root_hwnd or child_hwnd or None
        except Exception:
            return None

    def _get_window_title(self, hwnd):
        if not hasattr(ctypes, "windll") or not hwnd:
            return ""
        try:
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except Exception:
            return ""

    def _flat_button(self, parent, text, command, width=10, **kwargs):
        opts = dict(relief="flat", bg=COLOR_BTN_IDLE, activebackground=COLOR_BTN_IDLE_ACTIVE,
                    fg=COLOR_TEXT, bd=1, cursor="hand2", width=width,
                    takefocus=0, highlightthickness=0)
        opts.update(kwargs)
        return tk.Button(parent, text=text, command=command, **opts)

    def _set_toggle_running_style(self, btn, running):
        if running:
            btn.config(bg=COLOR_STOP, fg="white", activebackground=COLOR_STOP_ACTIVE,
                       activeforeground="white")
        else:
            btn.config(bg=COLOR_START, fg=COLOR_TEXT, activebackground=COLOR_START_ACTIVE,
                       activeforeground=COLOR_TEXT)

    def _add_save_cancel_buttons(self, parent, row, on_ok, on_cancel):
        btn_row = tk.Frame(parent, bg=COLOR_CARD)
        btn_row.grid(row=row, column=0, columnspan=2, pady=(6, 10))
        tk.Button(btn_row, text="Save", command=on_ok, width=8, relief="flat",
                  bg=COLOR_START, activebackground=COLOR_START_ACTIVE, fg=COLOR_TEXT, bd=1,
                  cursor="hand2", takefocus=0, highlightthickness=0).pack(side="left", padx=4)
        tk.Button(btn_row, text="Cancel", command=on_cancel, width=8, relief="flat",
                  bg=COLOR_BTN_IDLE, activebackground=COLOR_BTN_IDLE_ACTIVE, fg=COLOR_TEXT, bd=1,
                  cursor="hand2", takefocus=0, highlightthickness=0).pack(side="left", padx=4)
        return btn_row

    def create_hotkey_and_toggle_row(self, parent, default_hotkey, toggle_command, action_label, hotkey_which,
                                      running_attr, target=None, running_attr_getter=None):
        row = tk.Frame(parent, bg=COLOR_CARD)
        row.pack(fill="x", pady=(8, 0))

        ttk.Label(row, text="Hotkey:").pack(side="left")
        hotkey_entry = ttk.Entry(row, width=10, justify="center", state="readonly")
        hotkey_entry.pack(side="left", padx=(4, 4))
        hotkey_entry.configure(state="normal")
        hotkey_entry.insert(0, default_hotkey)
        hotkey_entry.configure(state="readonly")

        set_btn = self._flat_button(row, "Set Hotkey", lambda: self.start_hotkey_capture(hotkey_which), width=10)
        set_btn.pack(side="left", padx=(0, 10))

        toggle_btn = tk.Button(row, text=f"Start {action_label} ({default_hotkey.upper()})",
                                command=toggle_command, bg=COLOR_START, fg=COLOR_TEXT,
                                font=("Segoe UI", 9, "bold"), relief="flat",
                                activebackground=COLOR_START_ACTIVE, activeforeground=COLOR_TEXT, bd=1,
                                width=20, pady=4, cursor="hand2", takefocus=0, highlightthickness=0)
        toggle_btn.pack(side="right", fill="x", expand=True)

        self.hotkey_specs[hotkey_which] = {
            'entry': hotkey_entry,
            'btn': toggle_btn,
            'toggle': toggle_command,
            'running_attr': running_attr,
            'target': target if target is not None else self,
            'running_attr_getter': running_attr_getter,
            'label': action_label,
            'registered': None,
            'registered_handle': None,
        }

        return hotkey_entry, toggle_btn

    def start_hotkey_capture(self, which):
        if self.capturing_hotkey_for is not None:
            return
        if not _INPUT_LIBS_READY.is_set():
            return

        self.capturing_hotkey_for = which
        entry = self.hotkey_specs[which]['entry']
        self._hotkey_capture_prev_value = entry.get()
        self._set_entry_text(entry, "Press a key... (Esc to cancel)", readonly=True)

        try:
            self._hotkey_capture_hook = keyboard.hook(self._on_hotkey_capture_key_event, suppress=False)
        except Exception as e:
            self.capturing_hotkey_for = None
            self._set_entry_text(entry, self._hotkey_capture_prev_value, readonly=True)
            return

        self._hotkey_capture_timeout_id = self.root.after(
            8000, lambda: self._cancel_hotkey_capture(which, timed_out=True))

    def _on_hotkey_capture_key_event(self, event):
        try:
            if event.event_type != "down":
                return
            which = self.capturing_hotkey_for
            if which is None:
                return
            self.root.after(0, lambda w=which, name=event.name: self._resolve_hotkey_capture(w, name))
        except Exception:
            pass

    def _resolve_hotkey_capture(self, which, key_name):
        if self.capturing_hotkey_for != which:
            return
        if key_name == "esc":
            self._cancel_hotkey_capture(which, timed_out=False)
            return
        self._teardown_hotkey_capture_hook()
        entry = self.hotkey_specs[which]['entry']
        self._set_entry_text(entry, key_name, readonly=True)
        self.capturing_hotkey_for = None
        self._register_hotkey(which)
        self.refresh_toggle_button_label(which)

    def _cancel_hotkey_capture(self, which, timed_out=False):
        if self.capturing_hotkey_for != which:
            return
        self._teardown_hotkey_capture_hook()
        entry = self.hotkey_specs[which]['entry']
        self._set_entry_text(entry, self._hotkey_capture_prev_value or "", readonly=True)
        self.capturing_hotkey_for = None
        self.refresh_toggle_button_label(which)

    def _teardown_hotkey_capture_hook(self):
        if self._hotkey_capture_timeout_id is not None:
            try:
                self.root.after_cancel(self._hotkey_capture_timeout_id)
            except Exception:
                pass
            self._hotkey_capture_timeout_id = None
        if self._hotkey_capture_hook is not None:
            try:
                keyboard.unhook(self._hotkey_capture_hook)
            except Exception:
                try:
                    keyboard.unhook(self._on_hotkey_capture_key_event)
                except Exception:
                    pass
            self._hotkey_capture_hook = None

    def refresh_toggle_button_label(self, which):
        spec = self.hotkey_specs[which]
        if spec.get('running_attr_getter') is not None:
            running = spec['running_attr_getter']()
        else:
            running = getattr(spec.get('target', self), spec['running_attr'])
        hotkey = spec['entry'].get().strip().upper() or "?"
        label = spec['label']
        btn = spec['btn']

        if running:
            btn.config(text=f"Stop {label} ({hotkey})")
        else:
            btn.config(text=f"Start {label} ({hotkey})")

    def start_pick_location(self, x_entry=None, y_entry=None, on_done=None):
        if x_entry is None:
            x_entry = self.x_display
        if y_entry is None:
            y_entry = self.y_display

        overlay = tk.Toplevel(self.root)
        overlay.attributes("-fullscreen", True)
        try:
            overlay.attributes("-alpha", 0.35)
        except tk.TclError:
            pass
        try:
            overlay.attributes("-topmost", True)
        except tk.TclError:
            pass
        overlay.configure(bg="black")
        overlay.config(cursor="crosshair")

        hint = tk.Label(overlay, text="Click anywhere to set the position  \u2022  Press ESC to cancel",
                         bg="black", fg="white", font=("Segoe UI", 12, "bold"))
        hint.place(relx=0.5, rely=0.05, anchor="n")

        def finish():
            overlay.destroy()
            if on_done is not None:
                on_done()

        def on_click(event):
            x, y = event.x_root, event.y_root
            x_entry.delete(0, tk.END)
            x_entry.insert(0, str(x))
            y_entry.delete(0, tk.END)
            y_entry.insert(0, str(y))
            finish()

        def on_cancel(event=None):
            finish()

        overlay.bind("<Button-1>", on_click)
        overlay.bind("<Escape>", on_cancel)
        overlay.focus_force()

    def get_total_interval(self, vars_dict):
        try:
            h = float(vars_dict['h'].get() or 0)
            m = float(vars_dict['m'].get() or 0)
            s = float(vars_dict['s'].get() or 0)
            ms = float(vars_dict['ms'].get() or 0)
            total_ms = (h * 3600 + m * 60 + s) * 1000 + ms
        except ValueError:
            total_ms = 100.0

        if vars_dict['rand_var'].get():
            try:
                rand_val = float(vars_dict['rand_ms'].get() or 0)
                total_ms += random.uniform(-rand_val, rand_val)
            except ValueError:
                pass

        if total_ms < 1:
            total_ms = 1
        return total_ms / 1000.0

    def get_effective_interval(self, vars_dict, max_speed_enabled, max_rate_entry):
        if max_speed_enabled:
            try:
                max_rate = float(max_rate_entry.get() or 0)
            except ValueError:
                max_rate = 0
            if max_rate > 0:
                interval = 1.0 / max_rate
                if vars_dict.get('rand_var') is not None and vars_dict['rand_var'].get():
                    try:
                        rand_val = float(vars_dict['rand_ms'].get() or 0) / 1000.0
                        interval += random.uniform(-rand_val, rand_val)
                    except ValueError:
                        pass
                return max(interval, 0.0005)
        return self.get_total_interval(vars_dict)

    def _interruptible_sleep(self, duration, running_attr):
        end_time = time.time() + max(duration, 0)
        while True:
            remaining = end_time - time.time()
            if remaining <= 0:
                return True
            if not getattr(self, running_attr):
                return False
            time.sleep(min(0.05, remaining))

    def _interruptible_sleep_event(self, duration, stop_event):
        return not stop_event.wait(max(duration, 0))

    def _set_entry_text(self, entry, value, readonly=False):
        try:
            if readonly:
                entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            if readonly:
                entry.configure(state="readonly")
        except Exception:
            pass

    def _interval_settings(self, vars_dict):
        return {
            'h': vars_dict['h'].get(),
            'm': vars_dict['m'].get(),
            's': vars_dict['s'].get(),
            'ms': vars_dict['ms'].get(),
            'rand': bool(vars_dict['rand_var'].get()),
            'rand_ms': vars_dict['rand_ms'].get(),
        }

    def _apply_interval_settings(self, vars_dict, data):
        if not data:
            return
        for key in ('h', 'm', 's', 'ms', 'rand_ms'):
            if key in data:
                self._set_entry_text(vars_dict[key], data[key])
        if 'rand' in data:
            vars_dict['rand_var'].set(bool(data['rand']))

    def get_settings_dict(self):
        data = {'version': 1}

        try:
            data['click'] = {
                'interval': self._interval_settings(self.click_int_vars),
                'hold_interval': self._interval_settings(self.click_hold_vars),
                'mouse_button': self.mouse_btn_var.get(),
                'click_type': self.click_type_var.get(),
                'action_mode': self.click_action_mode_var.get(),
                'smart_click': bool(self.smart_click_var.get()),
                'max_speed_enabled': bool(self.click_max_speed_var.get()),
                'max_cps': self.click_max_cps_entry.get(),
                'repeat_mode': self.repeat_mode_var.get(),
                'repeat_count': self.repeat_entry.get(),
                'pos_mode': self.pos_mode_var.get(),
                'x': self.x_display.get(),
                'y': self.y_display.get(),
                'hotkey': self.click_hotkey_entry.get(),
            }
        except Exception:
            pass

        try:
            data['press'] = {
                'interval': self._interval_settings(self.press_int_vars),
                'hold_interval': self._interval_settings(self.press_hold_vars),
                'key': self.press_key_var.get(),
                'press_type': self.press_type_var.get(),
                'mod_ctrl': self.press_mod_ctrl_var.get(),
                'mod_alt': self.press_mod_alt_var.get(),
                'mod_win': self.press_mod_win_var.get(),
                'mod_shift': self.press_mod_shift_var.get(),
                'action_mode': self.press_action_mode_var.get(),
                'block_physical_key': bool(self.block_physical_key_var.get()),
                'pause_on_window_switch': bool(self.pause_on_window_switch_var.get()),
                'max_speed_enabled': bool(self.press_max_speed_var.get()),
                'max_pps': self.press_max_pps_entry.get(),
                'repeat_mode': self.press_repeat_mode_var.get(),
                'repeat_count': self.press_repeat_entry.get(),
                'hotkey': self.press_hotkey_entry.get(),
            }
        except Exception:
            pass

        try:
            data['record'] = {
                'record_moves': bool(self.record_moves_var.get()),
                'record_keys': bool(self.record_keys_var.get()),
                'move_interval_ms': self.record_move_interval_entry.get(),
                'hotkey': self.record_hotkey_entry.get(),
            }
        except Exception:
            pass

        try:
            data['playback'] = {
                'repeat_mode': self.playback_repeat_mode_var.get(),
                'repeat_count': self.playback_repeat_entry.get(),
                'speed': self.playback_speed_entry.get(),
                'hotkey': self.playback_hotkey_entry.get(),
            }
        except Exception:
            pass

        try:
            data['pixel_watchers'] = [self._pixel_watcher_to_dict(w) for w in self.pixel_watchers]
        except Exception:
            pass

        return data

    def _record_ctx_events(self, owner):
        if owner is self._active_record_owner:
            return self.recorded_events
        if owner is None:
            return self._global_record_store.get('recorded_events', self.recorded_events)
        return owner.recorded_events

    def _pixel_watcher_to_dict(self, watcher):
        return {
            'title': watcher.title,
            'x': watcher.x_entry.get(),
            'y': watcher.y_entry.get(),
            'mode': watcher.mode_var.get(),
            'target_hex': watcher.target_hex_entry.get(),
            'tolerance': watcher.tolerance_entry.get(),
            'interval_ms': watcher.interval_entry.get(),
            'cooldown_s': watcher.cooldown_entry.get(),
            'stop_after_trigger': bool(watcher.stop_after_trigger_var.get()),
            'recorded_events': list(self._record_ctx_events(watcher)),
            'record_hotkey': watcher.record_hotkey_entry.get() if watcher.record_hotkey_entry else '',
            'playback_hotkey': watcher.playback_hotkey_entry.get() if watcher.playback_hotkey_entry else '',
            'playback_repeat_mode': watcher.playback_repeat_mode_var.get(),
            'playback_repeat_count': watcher.playback_repeat_entry.get(),
            'playback_speed': watcher.playback_speed_entry.get(),
        }

    def apply_settings_dict(self, data):
        if not isinstance(data, dict):
            return

        click = data.get('click') or {}
        try:
            self._apply_interval_settings(self.click_int_vars, click.get('interval'))
            self._apply_interval_settings(self.click_hold_vars, click.get('hold_interval'))
            if 'mouse_button' in click:
                self.mouse_btn_var.set(click['mouse_button'])
            if 'click_type' in click:
                self.click_type_var.set(click['click_type'])
            if 'action_mode' in click:
                self.click_action_mode_var.set(click['action_mode'])
            if 'smart_click' in click:
                self.smart_click_var.set(bool(click['smart_click']))
            if 'max_speed_enabled' in click:
                self.click_max_speed_var.set(bool(click['max_speed_enabled']))
            if 'max_cps' in click:
                self._set_entry_text(self.click_max_cps_entry, click['max_cps'])
            if 'repeat_mode' in click:
                self.repeat_mode_var.set(click['repeat_mode'])
            if 'repeat_count' in click:
                self._set_entry_text(self.repeat_entry, click['repeat_count'])
            if 'pos_mode' in click:
                self.pos_mode_var.set(click['pos_mode'])
            if 'x' in click:
                self._set_entry_text(self.x_display, click['x'])
            if 'y' in click:
                self._set_entry_text(self.y_display, click['y'])
            if click.get('hotkey'):
                self._set_entry_text(self.click_hotkey_entry, click['hotkey'], readonly=True)
            self.on_click_max_speed_toggle()
            self.refresh_toggle_button_label("click")
        except Exception:
            pass

        press = data.get('press') or {}
        try:
            self._apply_interval_settings(self.press_int_vars, press.get('interval'))
            self._apply_interval_settings(self.press_hold_vars, press.get('hold_interval'))
            if 'key' in press:
                self.press_key_var.set(press['key'])
            if 'press_type' in press:
                self.press_type_var.set(press['press_type'])
            if 'mod_ctrl' in press:
                self.press_mod_ctrl_var.set(bool(press['mod_ctrl']))
            if 'mod_alt' in press:
                self.press_mod_alt_var.set(bool(press['mod_alt']))
            if 'mod_win' in press:
                self.press_mod_win_var.set(bool(press['mod_win']))
            if 'mod_shift' in press:
                self.press_mod_shift_var.set(bool(press['mod_shift']))
            if 'action_mode' in press:
                self.press_action_mode_var.set(press['action_mode'])
            if 'block_physical_key' in press:
                self.block_physical_key_var.set(bool(press['block_physical_key']))
            if 'pause_on_window_switch' in press:
                self.pause_on_window_switch_var.set(bool(press['pause_on_window_switch']))
            if 'max_speed_enabled' in press:
                self.press_max_speed_var.set(bool(press['max_speed_enabled']))
            if 'max_pps' in press:
                self._set_entry_text(self.press_max_pps_entry, press['max_pps'])
            if 'repeat_mode' in press:
                self.press_repeat_mode_var.set(press['repeat_mode'])
            if 'repeat_count' in press:
                self._set_entry_text(self.press_repeat_entry, press['repeat_count'])
            if press.get('hotkey'):
                self._set_entry_text(self.press_hotkey_entry, press['hotkey'], readonly=True)
            self.on_press_max_speed_toggle()
            self.refresh_toggle_button_label("press")
        except Exception:
            pass

        record = data.get('record') or {}
        try:
            if 'record_moves' in record:
                self.record_moves_var.set(bool(record['record_moves']))
            if 'record_keys' in record:
                self.record_keys_var.set(bool(record['record_keys']))
            if record.get('move_interval_ms'):
                self._set_entry_text(self.record_move_interval_entry, str(record['move_interval_ms']))
            if record.get('hotkey'):
                self._set_entry_text(self.record_hotkey_entry, record['hotkey'], readonly=True)
            self.refresh_toggle_button_label("record")
        except Exception:
            pass

        playback = data.get('playback') or {}
        try:
            if 'repeat_mode' in playback:
                self.playback_repeat_mode_var.set(playback['repeat_mode'])
            if 'repeat_count' in playback:
                self._set_entry_text(self.playback_repeat_entry, playback['repeat_count'])
            if 'speed' in playback:
                self._set_entry_text(self.playback_speed_entry, playback['speed'])
            if playback.get('hotkey'):
                self._set_entry_text(self.playback_hotkey_entry, playback['hotkey'], readonly=True)
            self.refresh_toggle_button_label("playback")
        except Exception:
            pass

        try:
            self._rebuild_pixel_watchers_from_settings(data)
        except Exception:
            pass

    def _rebuild_pixel_watchers_from_settings(self, data):
        if not hasattr(self, 'pixel_watch_list'):
            return

        watcher_dicts = data.get('pixel_watchers')
        if not isinstance(watcher_dicts, list):
            legacy = data.get('pixel_watch')
            watcher_dicts = [legacy] if isinstance(legacy, dict) else []

        for w in list(self.pixel_watchers):
            if w.running and w.stop_event is not None:
                w.running = False
                w.stop_event.set()
            if w is self._active_record_owner:
                self.recording = False
                self.playing = False
                self._use_record_ctx(None)
            for which in (w.hotkey_which, self._record_hotkey_which(w, "record"),
                          self._record_hotkey_which(w, "playback")):
                spec = self.hotkey_specs.pop(which, None)
                if spec is not None and spec.get('registered_handle') is not None:
                    try:
                        keyboard.remove_hotkey(spec['registered_handle'])
                    except Exception:
                        pass
            if w.window is not None:
                w.window.destroy()
            if w.card is not None:
                w.card.destroy()
        self.pixel_watchers = []

        for wd in watcher_dicts:
            self._add_pixel_watcher(restore=wd if isinstance(wd, dict) else {})

        self._use_record_ctx(None)

    def _apply_pixel_watcher_dict(self, watcher, pixel_watch):
        if 'x' in pixel_watch:
            self._set_entry_text(watcher.x_entry, pixel_watch['x'])
        if 'y' in pixel_watch:
            self._set_entry_text(watcher.y_entry, pixel_watch['y'])
        if 'mode' in pixel_watch:
            watcher.mode_var.set(pixel_watch['mode'])
        if 'target_hex' in pixel_watch:
            self._set_entry_text(watcher.target_hex_entry, pixel_watch['target_hex'])
            self._sync_rgb_from_hex(watcher.target_hex_entry, watcher.target_r_entry,
                                     watcher.target_g_entry, watcher.target_b_entry, watcher.target_swatch)
        elif 'target_r' in pixel_watch or 'target_g' in pixel_watch or 'target_b' in pixel_watch:
            # Backward compatibility with profiles saved before the hex color UI.
            try:
                r = int(pixel_watch.get('target_r', 0) or 0)
                g = int(pixel_watch.get('target_g', 0) or 0)
                b = int(pixel_watch.get('target_b', 0) or 0)
                hexcode = f"#{r:02x}{g:02x}{b:02x}"
            except (TypeError, ValueError):
                hexcode = "#ff0000"
            self._set_entry_text(watcher.target_hex_entry, hexcode)
            self._sync_rgb_from_hex(watcher.target_hex_entry, watcher.target_r_entry,
                                     watcher.target_g_entry, watcher.target_b_entry, watcher.target_swatch)
        if 'tolerance' in pixel_watch:
            self._set_entry_text(watcher.tolerance_entry, pixel_watch['tolerance'])
        if 'interval_ms' in pixel_watch:
            self._set_entry_text(watcher.interval_entry, pixel_watch['interval_ms'])
        if 'cooldown_s' in pixel_watch:
            self._set_entry_text(watcher.cooldown_entry, pixel_watch['cooldown_s'])
        if 'stop_after_trigger' in pixel_watch:
            watcher.stop_after_trigger_var.set(bool(pixel_watch['stop_after_trigger']))
        if 'playback_repeat_mode' in pixel_watch:
            watcher.playback_repeat_mode_var.set(pixel_watch['playback_repeat_mode'])
        if 'playback_repeat_count' in pixel_watch:
            self._set_entry_text(watcher.playback_repeat_entry, pixel_watch['playback_repeat_count'])
        if 'playback_speed' in pixel_watch:
            self._set_entry_text(watcher.playback_speed_entry, pixel_watch['playback_speed'])
        if pixel_watch.get('record_hotkey') and watcher.record_hotkey_entry is not None:
            self._set_entry_text(watcher.record_hotkey_entry, pixel_watch['record_hotkey'], readonly=True)
        if pixel_watch.get('playback_hotkey') and watcher.playback_hotkey_entry is not None:
            self._set_entry_text(watcher.playback_hotkey_entry, pixel_watch['playback_hotkey'], readonly=True)

        events = pixel_watch.get('recorded_events')
        if not isinstance(events, list):
            events = pixel_watch.get('actions')
        if isinstance(events, list):
            valid_types = {'key', 'button', 'move', 'wheel'}
            cleaned = [ev for ev in events if isinstance(ev, dict) and ev.get('type') in valid_types
                       and 'time' in ev]
            if self._use_record_ctx(watcher):
                self.recorded_events = cleaned
                self._refresh_recorded_list()
            else:
                watcher.recorded_events = cleaned

        if pixel_watch.get('title'):
            watcher.title = pixel_watch['title']
            if watcher.card_title_label is not None:
                watcher.card_title_label.config(text=watcher.title)
            if watcher.window is not None:
                watcher.window.title(watcher.title)
        self._on_pixel_mode_changed(watcher)
        self._refresh_pixel_watch_buttons(watcher)
        self.refresh_toggle_button_label(self._record_hotkey_which(watcher, "record"))
        self.refresh_toggle_button_label(self._record_hotkey_which(watcher, "playback"))

    def _safe_filename(self, name):
        cleaned = re.sub(r'[\\/:*?"<>|]+', "_", (name or "").strip())
        cleaned = re.sub(r'\s+', "_", cleaned).strip("_")
        return cleaned or "watcher"

    def _download_pixel_watcher(self, watcher):
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Download Watcher",
            defaultextension=".json",
            filetypes=[("JSON file", "*.json"), ("All files", "*.*")],
            initialfile=f"4FAutoClicker_watcher_{self._safe_filename(watcher.title)}.json",
        )
        if not path:
            return
        try:
            data = {'type': '4fautoclicker_watcher', 'version': 1, 'watcher': self._pixel_watcher_to_dict(watcher)}
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as exc:
            messagebox.showerror("Download failed", f"Could not save the file:\n{exc}", parent=self.root)
            return
        messagebox.showinfo("Download", "Watcher saved successfully.", parent=self.root)

    def _import_pixel_watcher(self, watcher):
        path = filedialog.askopenfilename(
            parent=self.root, title="Import Watcher", filetypes=[("JSON file", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as exc:
            messagebox.showerror("Import failed", f"Could not read the file:\n{exc}", parent=self.root)
            return

        watcher_data = data.get('watcher') if isinstance(data, dict) else None
        if not isinstance(watcher_data, dict):
            messagebox.showerror("Import failed", "This file doesn't contain a valid watcher.", parent=self.root)
            return

        if not messagebox.askyesno(
                "Import Watcher",
                f"Replace the settings of \"{watcher.title}\" with the imported watcher?",
                parent=self.root):
            return
        self._apply_pixel_watcher_dict(watcher, watcher_data)

    def save_profiles_store(self):
        try:
            data = {
                'version': 1,
                'active': self.active_profile_name,
                'profiles': self.profiles,
                'auto_save': bool(self.auto_save_var.get()) if hasattr(self, 'auto_save_var') else False,
            }
            with open(self.profiles_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))
        except Exception:
            pass

    def load_profiles_store(self):
        data = None
        try:
            with open(self.profiles_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = None

        if isinstance(data, dict) and isinstance(data.get('profiles'), dict) and data['profiles']:
            self.profiles = data['profiles']
            active = data.get('active')
            self.active_profile_name = active if active in self.profiles else next(iter(self.profiles))
            self.auto_save_var.set(bool(data.get('auto_save', False)))
        else:
            migrated = None
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    migrated = json.load(f)
            except Exception:
                migrated = None
            self.profiles = {'Default': migrated if isinstance(migrated, dict) else self.get_settings_dict()}
            self.active_profile_name = 'Default'
            self.save_profiles_store()

        try:
            self.apply_settings_dict(self.profiles[self.active_profile_name])
        except Exception:
            pass
        self._reregister_all_hotkeys()
        self.refresh_profile_list()

    def on_close(self):
        try:
            self._teardown_hotkey_capture_hook()
            self.capturing_hotkey_for = None
        except Exception:
            pass
        try:
            if self.clicker_running and getattr(self, 'clicker_stop_event', None) is not None:
                self.clicker_stop_event.set()
            if self.presser_running and getattr(self, 'presser_stop_event', None) is not None:
                self.presser_stop_event.set()
            for w in getattr(self, 'pixel_watchers', []):
                if w.running and w.stop_event is not None:
                    w.stop_event.set()
            self.playing = False
        except Exception:
            pass
        try:
            if keyboard is not None:
                keyboard.unhook_all()
            if mouse is not None:
                mouse.unhook_all()
        except Exception:
            pass
        try:
            self._autosave_active_profile()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def toggle_clicker(self):
        if not self.clicker_running:
            self.clicker_gen += 1
            gen = self.clicker_gen
            stop_event = threading.Event()
            self.clicker_stop_event = stop_event
            self.clicker_running = True
            self._set_toggle_running_style(self.click_toggle_btn, True)
            self.refresh_toggle_button_label("click")
            self.clicker_thread = threading.Thread(target=self.run_clicker, args=(gen, stop_event), daemon=True)
            self.clicker_thread.start()
        else:
            self.clicker_running = False
            if self.clicker_stop_event is not None:
                self.clicker_stop_event.set()
            self._set_toggle_running_style(self.click_toggle_btn, False)
            self.refresh_toggle_button_label("click")

    def toggle_presser(self):
        if not self.presser_running:
            self.presser_gen += 1
            gen = self.presser_gen
            stop_event = threading.Event()
            self.presser_stop_event = stop_event
            self.presser_running = True
            self._set_toggle_running_style(self.press_toggle_btn, True)
            self.refresh_toggle_button_label("press")
            self.presser_thread = threading.Thread(target=self.run_presser, args=(gen, stop_event), daemon=True)
            self.presser_thread.start()
        else:
            self.presser_running = False
            if self.presser_stop_event is not None:
                self.presser_stop_event.set()
            self._set_toggle_running_style(self.press_toggle_btn, False)
            self.refresh_toggle_button_label("press")

    def _record_hotkey_which(self, owner, kind):
        return kind if owner is None else f"{kind}_w{owner.id}"

    def _record_running_attr_value(self, owner, running_attr):
        if owner is self._active_record_owner:
            return bool(getattr(self, running_attr))
        if owner is None:
            return bool(self._global_record_store.get(running_attr, False))
        return bool(getattr(owner, running_attr, False))

    def _use_record_ctx(self, owner):
        if owner is self._active_record_owner:
            return True
        if self.recording or self.playing:
            return False

        prev_owner = self._active_record_owner
        if prev_owner is None:
            for name in RECORD_CTX_ATTRS:
                self._global_record_store[name] = getattr(self, name)
        else:
            for name in RECORD_CTX_ATTRS:
                setattr(prev_owner, name, getattr(self, name))

        if owner is None:
            for name in RECORD_CTX_ATTRS:
                setattr(self, name, self._global_record_store[name])
        else:
            for name in RECORD_CTX_ATTRS:
                setattr(self, name, getattr(owner, name))

        self._active_record_owner = owner
        return True

    def _with_record_ctx(self, owner, fn):
        def wrapped(*args, **kwargs):
            if self._use_record_ctx(owner):
                return fn(*args, **kwargs)
            return None
        return wrapped

    def toggle_recording(self):
        owner = self._active_record_owner
        which = self._record_hotkey_which(owner, "record")
        if self.playing:
            return
        if not self.recording:
            _INPUT_LIBS_READY.wait()
            self.recording = True
            self.recorded_events = []
            self.record_start_time = time.time()
            self._keys_held = set()
            self._buttons_held = set()
            self._last_move_record_wall = 0.0
            self._refresh_recorded_list()
            try:
                mouse.hook(self._on_mouse_event)
            except Exception:
                pass
            try:
                keyboard.hook(self._on_keyboard_event)
            except Exception:
                pass
            self._set_toggle_running_style(self.record_toggle_btn, True)
            self.refresh_toggle_button_label(which)
        else:
            self.recording = False
            try:
                mouse.unhook(self._on_mouse_event)
            except Exception:
                pass
            try:
                keyboard.unhook(self._on_keyboard_event)
            except Exception:
                pass
            self._close_open_hold_events(time.time() - self.record_start_time)
            self._keys_held = set()
            self._buttons_held = set()
            self._set_toggle_running_style(self.record_toggle_btn, False)
            self.refresh_toggle_button_label(which)
            self._refresh_recorded_list()

    def toggle_playback(self):
        owner = self._active_record_owner
        which = self._record_hotkey_which(owner, "playback")
        if self.recording:
            return
        if not self.playing:
            if not self.recorded_events:
                return
            if self.playback_thread is not None and self.playback_thread.is_alive():
                return
            self.playing = True
            self._set_toggle_running_style(self.playback_toggle_btn, True)
            self.refresh_toggle_button_label(which)
            self.playback_thread = threading.Thread(target=self.run_playback, args=(owner,), daemon=True)
            self.playback_thread.start()
        else:
            self.playing = False
            self._set_toggle_running_style(self.playback_toggle_btn, False)
            self.refresh_toggle_button_label(which)

    def toggle_pixel_watch(self, watcher):
        if not watcher.running:
            watcher.gen += 1
            gen = watcher.gen
            stop_event = threading.Event()
            watcher.stop_event = stop_event
            watcher.running = True
            self._refresh_pixel_watch_buttons(watcher)
            watcher.thread = threading.Thread(target=self.run_pixel_watch, args=(watcher, gen, stop_event),
                                               daemon=True)
            watcher.thread.start()
        else:
            watcher.running = False
            if watcher.stop_event is not None:
                watcher.stop_event.set()
            self._refresh_pixel_watch_buttons(watcher)

    def _refresh_pixel_watch_buttons(self, watcher):
        running = watcher.running
        if watcher.toggle_btn is not None:
            self._set_toggle_running_style(watcher.toggle_btn, running)
            self.refresh_toggle_button_label(watcher.hotkey_which)
        if watcher.card_toggle_btn is not None:
            self._set_toggle_running_style(watcher.card_toggle_btn, running)
            watcher.card_toggle_btn.config(text=("Stop Watching" if running else "Start Watching"))

    def clear_recorded_events(self):
        if self.recording or self.playing:
            return
        self.recorded_events.clear()
        self._record_row_map.clear()
        self.record_tree.delete(*self.record_tree.get_children())
        self._refresh_recorded_list()

    def _download_recorded_events(self):
        if self.recording or self.playing:
            return
        if not self.recorded_events:
            messagebox.showinfo("Download", "There are no recorded actions to download.", parent=self.root)
            return
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Download Recorded Actions",
            defaultextension=".json",
            filetypes=[("JSON file", "*.json"), ("All files", "*.*")],
            initialfile="4FAutoClicker_recorded_actions.json",
        )
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'recorded_events': self.recorded_events}, f, indent=2)
        except Exception as exc:
            messagebox.showerror("Download failed", f"Could not save the file:\n{exc}", parent=self.root)
            return
        messagebox.showinfo("Download", "Recorded actions saved successfully.", parent=self.root)

    def _import_recorded_events(self):
        if self.recording or self.playing:
            return
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Import Recorded Actions",
            filetypes=[("JSON file", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as exc:
            messagebox.showerror("Import failed", f"Could not read the file:\n{exc}", parent=self.root)
            return

        events = data.get('recorded_events') if isinstance(data, dict) else data
        if not isinstance(events, list):
            messagebox.showerror("Import failed", "This file doesn't contain valid recorded actions.",
                                  parent=self.root)
            return

        valid_types = {'key', 'button', 'move', 'wheel'}
        cleaned = []
        for ev in events:
            if isinstance(ev, dict) and ev.get('type') in valid_types and 'time' in ev:
                cleaned.append(ev)
        if not cleaned:
            messagebox.showerror("Import failed", "This file doesn't contain valid recorded actions.",
                                  parent=self.root)
            return

        replace = messagebox.askyesno(
            "Import",
            f"Found {len(cleaned)} action(s) in this file.\n\n"
            "Yes = replace the current list\nNo = add to the current list",
            parent=self.root,
        )
        if replace:
            self.recorded_events = cleaned
        else:
            self.recorded_events.extend(cleaned)
        self.recorded_events.sort(key=lambda e: e['time'])
        self._refresh_recorded_list()

    def _close_open_hold_events(self, stop_time):
        open_holds = {}
        for ev in self.recorded_events:
            if ev['type'] == 'key':
                hold_id = ('key', ev['name'])
            elif ev['type'] == 'button':
                hold_id = ('button', ev['button'])
            else:
                continue
            if ev['action'] == 'down':
                open_holds[hold_id] = True
            elif ev['action'] == 'up':
                open_holds.pop(hold_id, None)

        for kind, identifier in open_holds:
            if kind == 'key':
                self.recorded_events.append({'type': 'key', 'time': stop_time, 'name': identifier, 'action': 'up'})
            else:
                self.recorded_events.append(
                    {'type': 'button', 'time': stop_time, 'button': identifier, 'action': 'up'})

    def _get_move_record_interval_seconds(self):
        try:
            ms = int(float(self.record_move_interval_entry.get().strip()))
        except (ValueError, AttributeError):
            ms = DEFAULT_MOVE_RECORD_INTERVAL_MS
        if ms < MIN_MOVE_RECORD_INTERVAL_MS:
            ms = MIN_MOVE_RECORD_INTERVAL_MS
        return ms / 1000.0

    def _on_mouse_event(self, event):
        if not self.recording:
            return
        t = time.time() - self.record_start_time
        appended = False
        if isinstance(event, mouse.ButtonEvent):
            button = event.button
            action = event.event_type
            if action == 'down':
                if button in self._buttons_held:
                    return
                self._buttons_held.add(button)
            elif action == 'up':
                self._buttons_held.discard(button)
            self.recorded_events.append(
                {'type': 'button', 'time': t, 'button': button, 'action': action})
            appended = True
        elif isinstance(event, mouse.MoveEvent):
            if self.record_moves_var.get():
                now_wall = time.time()
                if now_wall - self._last_move_record_wall >= self._get_move_record_interval_seconds():
                    self._last_move_record_wall = now_wall
                    self.recorded_events.append({'type': 'move', 'time': t, 'x': event.x, 'y': event.y})
                    appended = True
        elif isinstance(event, mouse.WheelEvent):
            self.recorded_events.append({'type': 'wheel', 'time': t, 'delta': event.delta})
            appended = True
        if appended:
            self._schedule_count_label_update()

    def _on_keyboard_event(self, event):
        if not self.recording or not self.record_keys_var.get():
            return
        skip_names = set()
        owner = self._active_record_owner
        for kind in ('record', 'playback'):
            which = self._record_hotkey_which(owner, kind)
            try:
                skip_names.add(self.hotkey_specs[which]['entry'].get().strip().lower())
            except Exception:
                pass
        if event.name and event.name.lower() in skip_names:
            return

        name = event.name
        action = event.event_type
        if action == 'down':
            if name in self._keys_held:
                return
            self._keys_held.add(name)
        elif action == 'up':
            self._keys_held.discard(name)

        t = time.time() - self.record_start_time
        self.recorded_events.append({'type': 'key', 'time': t, 'name': name, 'action': action})
        self._schedule_count_label_update()

    def _schedule_count_label_update(self):
        if self._count_label_update_pending:
            return
        self._count_label_update_pending = True
        self._safe_ui_after(self._flush_count_label_update)

    def _flush_count_label_update(self):
        self._count_label_update_pending = False
        if self.recording:

            rows = self._compute_display_rows()
            self.record_count_label.config(text=f"Recorded events: {len(rows)}")

    def _compute_display_rows(self, events=None):
        rows = []
        open_holds = {}
        events = self.recorded_events if events is None else events
        n = len(events)
        i = 0

        while i < n:
            ev = events[i]
            t = ev['time']
            if ev['type'] == 'key':
                hold_id = ('key', ev['name'])
                if ev['action'] == 'down':
                    open_holds.setdefault(hold_id, (i, t))
                elif ev['action'] == 'up':
                    if hold_id in open_holds:
                        down_i, start_t = open_holds.pop(hold_id)
                        duration = t - start_t
                        if duration <= TAP_MAX_DURATION_S:
                            rows.append((('tap', down_i, i), f"{start_t:.2f}", "Key press",
                                         f"{ev['name']} press"))
                        else:
                            rows.append((('hold', down_i, i), f"{start_t:.2f}", "Key hold",
                                         f"{ev['name']} for {duration:.2f}s"))
                    else:
                        rows.append((('single', i), f"{t:.2f}", "Key", f"{ev['name']} up"))
                else:
                    rows.append((('single', i), f"{t:.2f}", "Key", f"{ev['name']} {ev['action']}"))
                i += 1
            elif ev['type'] == 'button':
                hold_id = ('button', ev['button'])
                if ev['action'] == 'down':
                    open_holds.setdefault(hold_id, (i, t))
                elif ev['action'] == 'up':
                    if hold_id in open_holds:
                        down_i, start_t = open_holds.pop(hold_id)
                        duration = t - start_t
                        if duration <= TAP_MAX_DURATION_S:
                            rows.append((('tap', down_i, i), f"{start_t:.2f}", "Mouse click",
                                         f"{ev['button']} click"))
                        else:
                            rows.append((('hold', down_i, i), f"{start_t:.2f}", "Mouse hold",
                                         f"{ev['button']} for {duration:.2f}s"))
                    else:
                        rows.append((('single', i), f"{t:.2f}", "Mouse", f"{ev['button']} up"))
                else:
                    rows.append((('single', i), f"{t:.2f}", "Mouse", f"{ev['button']} {ev['action']}"))
                i += 1
            elif ev['type'] == 'move':
                rows.append((('single', i), f"{t:.2f}", "Mouse move", f"({ev['x']}, {ev['y']})"))
                i += 1
            elif ev['type'] == 'wheel':
                sign = 1 if ev['delta'] >= 0 else -1
                end_i = i
                while (end_i + 1 < n and events[end_i + 1]['type'] == 'wheel'
                       and (1 if events[end_i + 1]['delta'] >= 0 else -1) == sign):
                    end_i += 1
                direction = "up" if sign > 0 else "down"
                duration = events[end_i]['time'] - t
                rows.append((('wheel_group', i, end_i), f"{t:.2f}", "Mouse wheel",
                             f"{direction} for {duration:.2f}s"))
                i = end_i + 1
            else:
                rows.append((('single', i), f"{t:.2f}", "Unknown", str(ev)))
                i += 1

        for (kind, identifier), (down_i, start_t) in open_holds.items():
            label = "Key hold" if kind == "key" else "Mouse hold"
            rows.append((('open_hold', down_i), f"{start_t:.2f}", label, f"{identifier} (not released)"))
        return rows

    def _refresh_recorded_list(self):
        rows = self._compute_display_rows()

        self.record_count_label.config(text=f"Recorded events: {len(rows)}")
        self.record_tree.delete(*self.record_tree.get_children())

        preview_limit = 300
        visible_rows = rows[:preview_limit]
        self._record_row_map = [row_key for row_key, *_ in visible_rows]
        for row_index, (_, t_str, type_str, detail_str) in enumerate(visible_rows):
            self.record_tree.insert("", tk.END, iid=str(row_index),
                                     values=(row_index + 1, t_str, type_str, detail_str))
        if len(rows) > preview_limit:
            self.record_tree.insert("", tk.END, iid="more",
                                     values=("", "", "", f"... and {len(rows) - preview_limit} more"))
        self.record_tree.insert("", tk.END, iid=RECORD_BLANK_ROW_IID, values=("", "", "", ""))

    def _indices_for_row_key(self, row_key):
        if row_key[0] in ("single", "open_hold"):
            return {row_key[1]}
        elif row_key[0] in ("hold", "tap"):
            return {row_key[1], row_key[2]}
        return set(range(row_key[1], row_key[2] + 1))

    def _on_record_tree_double_click(self, event):
        if self.recording or self.playing:
            return
        item = self.record_tree.identify_row(event.y)
        if item:
            self._open_event_editor(item)

    def _edit_selected_event(self):
        if self.recording or self.playing:
            return
        sel = self.record_tree.selection()
        if sel:
            self._open_event_editor(sel[0])

    def _delete_selected_event(self):
        if self.recording or self.playing:
            return
        sel = self.record_tree.selection()
        if not sel:
            return
        indices = self._event_indices_for_iid(sel[0])
        if not indices:
            return
        indices = set(indices)
        self.recorded_events = [ev for i, ev in enumerate(self.recorded_events) if i not in indices]
        self._refresh_recorded_list()

    def _event_indices_for_iid(self, iid):
        row_index = self._row_index_from_iid(iid)
        if row_index is None:
            return None
        row_key = self._record_row_map[row_index]
        return sorted(self._indices_for_row_key(row_key))

    def _show_record_context_menu(self, event):
        if self.recording or self.playing:
            return
        iid = self.record_tree.identify_row(event.y)
        on_row = bool(iid) and iid not in ("more", RECORD_BLANK_ROW_IID)
        if on_row:
            self.record_tree.selection_set(iid)

        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Copy", command=lambda: self._copy_event_at_iid(iid),
                          state="normal" if on_row else "disabled")
        menu.add_command(label="Paste", command=self._paste_clipboard_events,
                          state="normal" if (not on_row and self._action_clipboard) else "disabled")
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _copy_event_at_iid(self, iid):
        indices = self._event_indices_for_iid(iid)
        if not indices:
            return
        base_t = self.recorded_events[indices[0]]['time']
        self._action_clipboard = [
            {**self.recorded_events[i], 'time': self.recorded_events[i]['time'] - base_t}
            for i in indices
        ]

    def _paste_clipboard_events(self):
        if not self._action_clipboard or self.recording or self.playing:
            return
        base_t = self.recorded_events[-1]['time'] + MULTI_CLICK_GAP_S if self.recorded_events else 0.0
        for item in self._action_clipboard:
            new_ev = dict(item)
            new_ev['time'] = base_t + item['time']
            self.recorded_events.append(new_ev)
        self._refresh_recorded_list()

    def _row_index_from_iid(self, iid):
        if iid == "more":
            return None
        try:
            row_index = int(iid)
        except ValueError:
            return None
        if row_index >= len(self._record_row_map):
            return None
        return row_index

    def _safe_float(self, raw_value, fallback):
        try:
            return float(raw_value)
        except (TypeError, ValueError):
            return fallback

    def _safe_int(self, raw_value, fallback):
        try:
            return int(float(raw_value))
        except (TypeError, ValueError):
            return fallback

    def _prompt_fields(self, title, specs, over_widget=None, anchor_widget=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=COLOR_CARD)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.withdraw()

        vars_map = {}
        for row, spec in enumerate(specs):
            ttk.Label(dialog, text=spec['label'] + ":").grid(row=row, column=0, sticky="w", padx=8, pady=6)
            var = tk.StringVar(value=str(spec.get('default', '')))
            if spec['type'] == 'combobox':
                widget = ttk.Combobox(dialog, textvariable=var, values=spec['values'], width=16, state="readonly")
            else:
                widget = ttk.Entry(dialog, textvariable=var, width=18)
            widget.grid(row=row, column=1, sticky="w", padx=8, pady=6)
            vars_map[spec['key']] = var

        outcome = {'ok': False}

        def on_ok():
            outcome['ok'] = True
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        self._add_save_cancel_buttons(dialog, len(specs), on_ok, on_cancel)

        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        if anchor_widget is not None:
            self._position_dialog_near_widget(dialog, anchor_widget)
        elif over_widget is not None:
            self._position_dialog_over_widget(dialog, over_widget)
        dialog.deiconify()
        dialog.grab_set()
        self.root.wait_window(dialog)

        if not outcome['ok']:
            return None
        return {key: var.get() for key, var in vars_map.items()}

    def _add_action_field_specs(self, category, last_t):
        if category == "Key press":
            return [
                {'key': 'time', 'label': 'Time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
                {'key': 'name', 'label': 'Key', 'type': 'combobox', 'values': ALL_KEYS, 'default': "space"},
            ]
        if category == "Key hold":
            return [
                {'key': 'time', 'label': 'Start time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
                {'key': 'duration', 'label': 'Duration (s)', 'type': 'entry', 'default': "1.0"},
                {'key': 'name', 'label': 'Key', 'type': 'combobox', 'values': ALL_KEYS, 'default': "space"},
            ]
        if category == "Mouse click":
            return [
                {'key': 'time', 'label': 'Time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
                {'key': 'button', 'label': 'Button', 'type': 'combobox', 'values': ["left", "right", "middle"],
                 'default': "left"},
            ]
        if category == "Mouse hold":
            return [
                {'key': 'time', 'label': 'Start time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
                {'key': 'duration', 'label': 'Duration (s)', 'type': 'entry', 'default': "1.0"},
                {'key': 'button', 'label': 'Button', 'type': 'combobox', 'values': ["left", "right", "middle"],
                 'default': "left"},
            ]
        if category == "Mouse move":
            return [
                {'key': 'time', 'label': 'Time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
            ]
        return [
            {'key': 'time', 'label': 'Start time (s)', 'type': 'entry', 'default': f"{last_t:.3f}"},
            {'key': 'direction', 'label': 'Direction', 'type': 'combobox', 'values': ["up", "down"],
             'default': "up"},
            {'key': 'duration', 'label': 'Duration (s)', 'type': 'entry', 'default': "1.0"},
        ]

    def _position_dialog_near_widget(self, dialog, widget, gap=8):
        dialog.update_idletasks()
        dw = dialog.winfo_reqwidth()
        dh = dialog.winfo_reqheight()
        bx = widget.winfo_rootx()
        by = widget.winfo_rooty()
        bh = widget.winfo_height()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()

        x = bx
        y = by + bh + gap
        if y + dh > screen_h:
            y = by - dh - gap
        if x + dw > screen_w:
            x = screen_w - dw - gap
        x = max(0, x)
        y = max(0, y)
        dialog.geometry(f"+{x}+{y}")

    def _position_dialog_over_widget(self, dialog, widget):
        dialog.update_idletasks()
        dw = dialog.winfo_reqwidth()
        dh = dialog.winfo_reqheight()
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        ww = widget.winfo_width()
        wh = widget.winfo_height()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()

        x = wx + max(0, (ww - dw) // 2)
        y = wy + max(0, (wh - dh) // 2)
        x = max(0, min(x, screen_w - dw))
        y = max(0, min(y, screen_h - dh))
        dialog.geometry(f"+{x}+{y}")

    def _center_dialog_over_widget(self, dialog, widget):
        dialog.update_idletasks()
        dw = dialog.winfo_reqwidth()
        dh = dialog.winfo_reqheight()
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        ww = widget.winfo_width()
        wh = widget.winfo_height()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()

        cx = wx + ww // 2
        cy = wy + wh // 2
        x = cx - dw // 2
        y = cy - dh // 2
        x = max(0, min(x, screen_w - dw))
        y = max(0, min(y, screen_h - dh))
        dialog.geometry(f"+{x}+{y}")

    def _prompt_add_action(self, last_t, title="Add Action", initial_category=None, initial_values=None,
                            default_position=1, max_position=1):
        categories = ["Key press", "Key hold", "Mouse click", "Mouse hold", "Mouse move", "Mouse wheel"]
        initial_values = initial_values or {}

        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=COLOR_CARD)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.withdraw()

        category_var = tk.StringVar(value=initial_category if initial_category in categories else categories[0])
        ttk.Label(dialog, text="Action type:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=categories,
                                       width=16, state="readonly")
        category_combo.grid(row=0, column=1, sticky="w", padx=8, pady=6)

        max_position = max(1, int(max_position or 1))
        default_position = max(1, min(int(default_position or 1), max_position))
        position_var = tk.StringVar(value=str(default_position))
        ttk.Label(dialog, text="Position (#):").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        position_row = tk.Frame(dialog, bg=COLOR_CARD)
        position_row.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        position_entry = ttk.Entry(position_row, textvariable=position_var, width=6)
        position_entry.pack(side="left")
        ttk.Label(position_row, text=f"(1-{max_position})", style="Muted.TLabel").pack(side="left", padx=(6, 0))

        fields_frame = tk.Frame(dialog, bg=COLOR_CARD)
        fields_frame.grid(row=2, column=0, columnspan=2, sticky="we")

        state = {'vars': {}, 'widgets': {}}

        def do_pick_location():
            dialog.grab_release()

            def restore():
                dialog.deiconify()
                dialog.lift()
                dialog.grab_set()
                dialog.focus_force()

            self.start_pick_location(state['widgets']['x'], state['widgets']['y'], on_done=restore)

        def rebuild_fields(use_initial=False):
            for child in fields_frame.winfo_children():
                child.destroy()
            state['vars'] = {}
            state['widgets'] = {}
            overrides = initial_values if use_initial else {}
            specs = self._add_action_field_specs(category_var.get(), last_t)
            for row, spec in enumerate(specs):
                ttk.Label(fields_frame, text=spec['label'] + ":").grid(
                    row=row, column=0, sticky="w", padx=8, pady=6)
                default_val = overrides.get(spec['key'], spec.get('default', ''))
                var = tk.StringVar(value=str(default_val))
                if spec['type'] == 'combobox':
                    widget = ttk.Combobox(fields_frame, textvariable=var, values=spec['values'],
                                           width=16, state="readonly")
                else:
                    widget = ttk.Entry(fields_frame, textvariable=var, width=18)
                widget.grid(row=row, column=1, sticky="w", padx=8, pady=6)
                state['vars'][spec['key']] = var
                state['widgets'][spec['key']] = widget

            if category_var.get() == "Mouse move":
                row = len(specs)
                ttk.Label(fields_frame, text="Position:").grid(
                    row=row, column=0, sticky="w", padx=8, pady=6)
                pos_row = tk.Frame(fields_frame, bg=COLOR_CARD)
                pos_row.grid(row=row, column=1, sticky="w", padx=8, pady=6)

                self._flat_button(pos_row, "Pick", do_pick_location, width=6).pack(side="left")
                ttk.Label(pos_row, text="X:").pack(side="left", padx=(10, 2))
                x_var = tk.StringVar(value=str(overrides.get('x', '0')))
                x_entry = ttk.Entry(pos_row, textvariable=x_var, width=6)
                x_entry.pack(side="left")
                ttk.Label(pos_row, text="Y:").pack(side="left", padx=(6, 2))
                y_var = tk.StringVar(value=str(overrides.get('y', '0')))
                y_entry = ttk.Entry(pos_row, textvariable=y_var, width=6)
                y_entry.pack(side="left")

                state['vars']['x'] = x_var
                state['vars']['y'] = y_var
                state['widgets']['x'] = x_entry
                state['widgets']['y'] = y_entry

        category_combo.bind("<<ComboboxSelected>>", lambda *_a: rebuild_fields(use_initial=False))
        rebuild_fields(use_initial=bool(initial_category))

        outcome = {'ok': False}

        def on_ok():
            outcome['ok'] = True
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        self._add_save_cancel_buttons(dialog, 3, on_ok, on_cancel)

        dialog.protocol("WM_DELETE_WINDOW", on_cancel)

        self._position_dialog_over_widget(dialog, self.record_tree)
        dialog.deiconify()
        dialog.grab_set()

        self.root.wait_window(dialog)

        if not outcome['ok']:
            return None
        result = {key: var.get() for key, var in state['vars'].items()}
        result['category'] = category_var.get()
        try:
            position = int(float(position_var.get()))
        except (TypeError, ValueError):
            position = default_position
        result['position'] = max(1, min(position, max_position))
        return result

    def _events_from_action_result(self, result, fallback_t):
        category = result['category']
        events = []
        if category == "Key press":
            t = self._safe_float(result['time'], fallback_t)
            name = result['name'].strip() or "space"
            events.append({'type': 'key', 'time': t, 'name': name, 'action': 'down'})
            events.append({'type': 'key', 'time': t + 0.01, 'name': name, 'action': 'up'})
        elif category == "Key hold":
            t = self._safe_float(result['time'], fallback_t)
            dur = max(0.0, self._safe_float(result['duration'], 1.0))
            name = result['name'].strip() or "space"
            events.append({'type': 'key', 'time': t, 'name': name, 'action': 'down'})
            events.append({'type': 'key', 'time': t + dur, 'name': name, 'action': 'up'})
        elif category == "Mouse click":
            t = self._safe_float(result['time'], fallback_t)
            button = result['button']
            events.append({'type': 'button', 'time': t, 'button': button, 'action': 'down'})
            events.append({'type': 'button', 'time': t + 0.01, 'button': button, 'action': 'up'})
        elif category == "Mouse hold":
            t = self._safe_float(result['time'], fallback_t)
            dur = max(0.0, self._safe_float(result['duration'], 1.0))
            button = result['button']
            events.append({'type': 'button', 'time': t, 'button': button, 'action': 'down'})
            events.append({'type': 'button', 'time': t + dur, 'button': button, 'action': 'up'})
        elif category == "Mouse move":
            t = self._safe_float(result['time'], fallback_t)
            x = self._safe_int(result['x'], 0)
            y = self._safe_int(result['y'], 0)
            events.append({'type': 'move', 'time': t, 'x': x, 'y': y})
        else:
            t = self._safe_float(result['time'], fallback_t)
            delta = 1 if result['direction'] == "up" else -1
            duration = max(0.0, self._safe_float(result.get('duration', '0'), 0.0))
            tick_count = max(1, int(round(duration / WHEEL_TICK_GAP_S)) + 1)
            for i in range(tick_count):
                events.append({'type': 'wheel', 'time': t + i * WHEEL_TICK_GAP_S, 'delta': delta})
        return events

    def _reposition_events(self, new_events, position, exclude_indices=None):
        exclude_indices = exclude_indices or set()

        original_rows = self._compute_display_rows()
        slot_times = []
        other_groups = []
        for row_key, *_ in original_rows:
            idx = self._indices_for_row_key(row_key)
            slot_times.append(min(self.recorded_events[i]['time'] for i in idx))
            if not (set(idx) & exclude_indices):
                other_groups.append([self.recorded_events[i] for i in idx])

        position = max(1, min(int(position), len(other_groups) + 1))

        if len(slot_times) < len(other_groups) + 1:

            if not slot_times:
                new_time = 0.0
            elif position == 1:
                new_time = max(0.0, slot_times[0] - 0.05)
            elif position > len(slot_times):
                new_time = slot_times[-1] + 0.05
            else:
                new_time = (slot_times[position - 2] + slot_times[position - 1]) / 2.0
            slot_times.insert(position - 1, new_time)

        content_order = other_groups[:position - 1] + [new_events] + other_groups[position - 1:]

        for group, target_time in zip(content_order, slot_times):
            if not group:
                continue
            base_t = min(ev['time'] for ev in group)
            offset = target_time - base_t
            if offset:
                for ev in group:
                    ev['time'] += offset

        self.recorded_events = [ev for group in content_order for ev in group]
        self.recorded_events.sort(key=lambda e: e['time'])

    def _add_new_event(self):
        if self.recording or self.playing:
            return

        last_t = self.recorded_events[-1]['time'] if self.recorded_events else 0.0
        row_count = len(self._compute_display_rows())
        max_position = row_count + 1
        result = self._prompt_add_action(last_t, default_position=max_position, max_position=max_position)
        if result is None:
            return
        new_events = self._events_from_action_result(result, last_t)
        self._reposition_events(new_events, result['position'])
        self._refresh_recorded_list()

    def _open_event_editor(self, iid):
        row_index = self._row_index_from_iid(iid)
        if row_index is None:
            return
        row_key = self._record_row_map[row_index]
        kind = row_key[0]
        indices = self._indices_for_row_key(row_key)

        if kind == 'single':
            ev = self.recorded_events[row_key[1]]
            if ev['type'] == 'key':
                category = "Key press"
                initial_values = {'time': f"{ev['time']:.3f}", 'name': ev['name']}
            elif ev['type'] == 'button':
                category = "Mouse click"
                initial_values = {'time': f"{ev['time']:.3f}", 'button': ev['button']}
            elif ev['type'] == 'move':
                category = "Mouse move"
                initial_values = {'time': f"{ev['time']:.3f}", 'x': str(ev['x']), 'y': str(ev['y'])}
            else:
                return
            fallback_t = ev['time']

        elif kind == 'tap':
            down_ev = self.recorded_events[row_key[1]]
            if down_ev['type'] == 'key':
                category = "Key press"
                initial_values = {'time': f"{down_ev['time']:.3f}", 'name': down_ev['name']}
            else:
                category = "Mouse click"
                initial_values = {'time': f"{down_ev['time']:.3f}", 'button': down_ev['button']}
            fallback_t = down_ev['time']

        elif kind == 'hold':
            down_ev = self.recorded_events[row_key[1]]
            up_ev = self.recorded_events[row_key[2]]
            duration = up_ev['time'] - down_ev['time']
            if down_ev['type'] == 'key':
                category = "Key hold"
                initial_values = {'time': f"{down_ev['time']:.3f}", 'duration': f"{duration:.3f}",
                                   'name': down_ev['name']}
            else:
                category = "Mouse hold"
                initial_values = {'time': f"{down_ev['time']:.3f}", 'duration': f"{duration:.3f}",
                                   'button': down_ev['button']}
            fallback_t = down_ev['time']

        elif kind == 'open_hold':
            ev = self.recorded_events[row_key[1]]
            if ev['type'] == 'key':
                category = "Key hold"
                initial_values = {'time': f"{ev['time']:.3f}", 'name': ev['name']}
            else:
                category = "Mouse hold"
                initial_values = {'time': f"{ev['time']:.3f}", 'button': ev['button']}
            fallback_t = ev['time']

        elif kind == 'wheel_group':
            start_i, end_i = row_key[1], row_key[2]
            group = self.recorded_events[start_i:end_i + 1]
            start_t = group[0]['time']
            duration = group[-1]['time'] - group[0]['time']
            current_dir = "up" if group[0]['delta'] >= 0 else "down"
            category = "Mouse wheel"
            initial_values = {'time': f"{start_t:.3f}", 'direction': current_dir, 'duration': f"{duration:.3f}"}
            fallback_t = start_t
        else:
            return

        total_rows = len(self._record_row_map)
        result = self._prompt_add_action(fallback_t, title="Edit Action",
                                          initial_category=category, initial_values=initial_values,
                                          default_position=row_index + 1, max_position=total_rows)
        if result is None:
            return

        new_events = self._events_from_action_result(result, fallback_t)
        self._reposition_events(new_events, result['position'], exclude_indices=indices)
        self._refresh_recorded_list()

    def _execute_recorded_event(self, ev):
        try:
            if ev['type'] == 'move':
                mouse.move(ev['x'], ev['y'], absolute=True, duration=0)
            elif ev['type'] == 'button':
                if ev['action'] == 'down':
                    mouse.press(button=ev['button'])
                elif ev['action'] == 'up':
                    mouse.release(button=ev['button'])
                elif ev['action'] == 'double':
                    mouse.click(button=ev['button'])
            elif ev['type'] == 'wheel':
                mouse.wheel(ev['delta'])
            elif ev['type'] == 'key':
                if ev['action'] == 'down':
                    keyboard.press(ev['name'])
                elif ev['action'] == 'up':
                    keyboard.release(ev['name'])
        except Exception:
            pass

    def run_playback(self, owner=None):
        _INPUT_LIBS_READY.wait()
        self._interruptible_sleep(1.0, 'playing')

        btn = self.playback_toggle_btn
        which = self._record_hotkey_which(owner, "playback")

        events = list(self.recorded_events)
        is_finite = (self.playback_repeat_mode_var.get() == "finite")
        try:
            limit_val = int(self.playback_repeat_entry.get() or 1)
        except ValueError:
            limit_val = 1
        try:
            speed = float(self.playback_speed_entry.get() or 1.0)
            if speed <= 0:
                speed = 1.0
        except ValueError:
            speed = 1.0

        count = 0
        try:
            while self.playing:
                if is_finite and count >= limit_val:
                    break

                last_t = 0.0
                for ev in events:
                    if not self.playing:
                        break
                    wait = (ev['time'] - last_t) / speed
                    ok = self._interruptible_sleep(wait, 'playing')
                    if not ok:
                        break
                    last_t = ev['time']
                    self._execute_recorded_event(ev)

                count += 1
        finally:
            self.playing = False
            if self.playback_thread is threading.current_thread():
                self.playback_thread = None
            self._safe_ui_after(lambda b=btn: self._set_toggle_running_style(b, False))
            self._safe_ui_after(lambda w=which: self.refresh_toggle_button_label(w))

    def run_pixel_watch(self, watcher, gen, stop_event):
        try:
            x = int(watcher.x_entry.get())
            y = int(watcher.y_entry.get())
        except ValueError:
            self._safe_ui_after(lambda: messagebox.showerror(
                "Invalid Position", "Please enter valid X and Y coordinates.", parent=self.root))
            if gen == watcher.gen:
                watcher.running = False
                self._safe_ui_after(lambda: self._refresh_pixel_watch_buttons(watcher))
            return

        mode = watcher.mode_var.get()
        target = self._parse_hex_color(watcher.target_hex_entry.get())
        if target is None:
            target = (0, 0, 0)
        try:
            tolerance = max(0, int(watcher.tolerance_entry.get() or 0))
        except ValueError:
            tolerance = 0
        try:
            interval = max(0.02, float(watcher.interval_entry.get() or 200) / 1000.0)
        except ValueError:
            interval = 0.2
        try:
            cooldown = max(0.0, float(watcher.cooldown_entry.get() or 0))
        except ValueError:
            cooldown = 0.0
        stop_after_trigger = bool(watcher.stop_after_trigger_var.get())

        last_color = self._get_pixel_color(x, y)
        was_matching = self._color_matches(last_color, target, tolerance) if mode == "specific" else False
        last_preview_sent = last_color
        self._safe_ui_after(lambda c=last_color: self._update_pixel_preview(watcher, c))

        try:
            while (watcher.running and gen == watcher.gen
                   and not stop_event.is_set()):
                color = self._get_pixel_color(x, y)
                if color is not None:

                    if color != last_preview_sent:
                        self._safe_ui_after(lambda c=color: self._update_pixel_preview(watcher, c))
                        last_preview_sent = color

                    if mode == "any":
                        triggered = last_color is not None and color != last_color
                    else:
                        matching = self._color_matches(color, target, tolerance)
                        triggered = matching and not was_matching
                        was_matching = matching
                    last_color = color

                    if triggered:
                        self._fire_pixel_watch_action(watcher, stop_event, gen)
                        if stop_event.is_set() or gen != watcher.gen or not watcher.running:
                            break
                        if stop_after_trigger:
                            break

                        last_color = self._get_pixel_color(x, y)
                        was_matching = (self._color_matches(last_color, target, tolerance)
                                         if mode == "specific" else False)
                        if cooldown > 0 and not self._interruptible_sleep_event(cooldown, stop_event):
                            break
                        continue

                if not self._interruptible_sleep_event(interval, stop_event):
                    break
        finally:
            if gen == watcher.gen:
                watcher.running = False
                self._safe_ui_after(lambda: self._refresh_pixel_watch_buttons(watcher))

    def _fire_pixel_watch_action(self, watcher, stop_event, gen):
        if not self._record_ctx_events(watcher):
            return

        started = threading.Event()

        def _start():
            if stop_event.is_set() or gen != watcher.gen or not watcher.running:
                started.set()
                return
            if self.recording:

                self.root.after(150, _start)
                return
            if not self._use_record_ctx(watcher):
                self.root.after(150, _start)
                return
            if not self.playing:
                self.toggle_playback()
            started.set()

        self._safe_ui_after(_start)
        started.wait(timeout=3.0)

        while (self._record_running_attr_value(watcher, 'playing') and gen == watcher.gen
               and not stop_event.is_set()):
            stop_event.wait(0.1)

    def run_clicker(self, gen, stop_event):
        _INPUT_LIBS_READY.wait()

        count = 0
        is_finite = (self.repeat_mode_var.get() == "finite")
        try:
            limit_val = int(self.repeat_entry.get() or 100)
        except ValueError:
            limit_val = 100

        btn_type = self.mouse_btn_var.get().lower()
        clicks = {"Double": 2, "Triple": 3}.get(self.click_type_var.get(), 1)
        is_fixed = (self.pos_mode_var.get() == "fixed")
        is_hold = (self.click_action_mode_var.get() == "Hold")
        smart_click = self.smart_click_var.get()
        max_speed = self.click_max_speed_var.get()
        self.click_rate_counter.reset()

        fx = fy = 0
        if is_fixed:
            try:
                fx = int(self.x_display.get())
                fy = int(self.y_display.get())
            except ValueError:
                self._safe_ui_after(lambda: messagebox.showerror(
                    "Invalid Position", "Please enter valid X and Y coordinates.", parent=self.root))
                if gen == self.clicker_gen:
                    self.clicker_running = False
                    self.clicker_thread = None
                    self._safe_ui_after(lambda: self._set_toggle_running_style(self.click_toggle_btn, False))
                    self._safe_ui_after(lambda: self.refresh_toggle_button_label("click"))
                return

        base_x = base_y = None
        last_action_pos = None
        if smart_click:
            if is_fixed:
                base_x, base_y = fx, fy
            else:
                base_x, base_y = mouse.get_position()

        def smart_point():
            nonlocal base_x, base_y, last_action_pos
            if not is_fixed:
                cur_x, cur_y = mouse.get_position()
                if last_action_pos is None or abs(cur_x - last_action_pos[0]) > 1 or abs(cur_y - last_action_pos[1]) > 1:
                    base_x, base_y = cur_x, cur_y
            ox = random.uniform(-SMART_CLICK_RADIUS, SMART_CLICK_RADIUS)
            oy = random.uniform(-SMART_CLICK_RADIUS, SMART_CLICK_RADIUS)
            tx, ty = base_x + ox, base_y + oy
            last_action_pos = (int(round(tx)), int(round(ty)))
            return tx, ty

        try:
            while not stop_event.is_set():
                if is_finite and count >= limit_val:
                    break

                if is_hold:
                    if smart_click:
                        tx, ty = smart_point()
                        mouse.move(int(tx), int(ty), absolute=True, duration=0)
                    elif is_fixed:
                        mouse.move(fx, fy, absolute=True, duration=0)
                    mouse.press(button=btn_type)
                    held_ok = self._interruptible_sleep_event(
                        self.get_total_interval(self.click_hold_vars), stop_event)
                    mouse.release(button=btn_type)
                    if not held_ok:
                        break
                else:
                    if smart_click:
                        tx, ty = smart_point()
                        mouse.move(int(tx), int(ty), absolute=True, duration=0)
                    elif is_fixed:
                        mouse.move(fx, fy, absolute=True, duration=0)
                    self._fire_clicks(btn_type, clicks, stop_event)

                count += 1
                self.click_rate_counter.tick(1 if is_hold else clicks)

                gap_ok = self._interruptible_sleep_event(
                    self.get_effective_interval(self.click_int_vars, max_speed, self.click_max_cps_entry),
                    stop_event)
                if not gap_ok:
                    break
        finally:
            if is_hold:
                try:
                    mouse.release(button=btn_type)
                except Exception:
                    pass
            if gen == self.clicker_gen:
                self.clicker_running = False
                self.clicker_thread = None
                self._safe_ui_after(lambda: self._set_toggle_running_style(self.click_toggle_btn, False))
                self._safe_ui_after(lambda: self.refresh_toggle_button_label("click"))

    def run_presser(self, gen, stop_event):
        _INPUT_LIBS_READY.wait()

        count = 0
        is_finite = (self.press_repeat_mode_var.get() == "finite")
        try:
            limit_val = int(self.press_repeat_entry.get() or 100)
        except ValueError:
            limit_val = 100

        key_name = self.press_key_var.get().strip() or "space"
        presses = {"Double": 2, "Triple": 3}.get(self.press_type_var.get(), 1)
        is_hold = (self.press_action_mode_var.get() == "Hold")
        max_speed = self.press_max_speed_var.get()
        self.press_rate_counter.reset()

        mod_keys = []
        if self.press_mod_ctrl_var.get():
            mod_keys.append("ctrl")
        if self.press_mod_alt_var.get():
            mod_keys.append("alt")
        if self.press_mod_win_var.get():
            mod_keys.append("windows")
        if self.press_mod_shift_var.get():
            mod_keys.append("shift")

        block_enabled = bool(self.block_physical_key_var.get())
        self._press_block_handle = None

        def _set_block(enabled):
            if enabled and self._press_block_handle is None:
                try:
                    self._press_block_handle = keyboard.block_key(key_name)
                except Exception:
                    self._press_block_handle = None
            elif not enabled and self._press_block_handle is not None:
                try:
                    keyboard.unblock_key(self._press_block_handle)
                except Exception:
                    pass
                self._press_block_handle = None

        def _press_modifiers():
            for m in mod_keys:
                try:
                    keyboard.press(m)
                except Exception:
                    pass

        def _release_modifiers():
            for m in reversed(mod_keys):
                try:
                    keyboard.release(m)
                except Exception:
                    pass

        def _keyboard_press(name):
            _set_block(False)
            try:
                _press_modifiers()
                keyboard.press(name)
            except Exception:
                pass
            finally:
                _set_block(block_enabled)

        def _keyboard_release(name):
            _set_block(False)
            try:
                keyboard.release(name)
                _release_modifiers()
            except Exception:
                pass
            finally:
                _set_block(block_enabled)

        def _keyboard_send(name):
            _set_block(False)
            try:
                _press_modifiers()
                keyboard.send(name)
                _release_modifiers()
            except Exception:
                pass
            finally:
                _set_block(block_enabled)

        pause_on_switch = bool(self.pause_on_window_switch_var.get())
        own_hwnd = self._get_own_hwnd() if pause_on_switch else None
        initial_hwnd = self._get_foreground_hwnd() if pause_on_switch else None
        initial_title = self._get_window_title(initial_hwnd) if pause_on_switch else ""
        if pause_on_switch and initial_hwnd is None:
            pause_on_switch = False

        target_hwnd = None
        target_title = ""
        awaiting_target = False
        if pause_on_switch:
            if own_hwnd is not None and initial_hwnd == own_hwnd:
                awaiting_target = True
            else:
                target_hwnd = initial_hwnd
                target_title = initial_title
        self.presser_awaiting_target = awaiting_target

        def _set_paused(value):
            if self.presser_paused != value:
                self.presser_paused = value

        def _set_awaiting_target(value):
            if self.presser_awaiting_target != value:
                self.presser_awaiting_target = value

        try:
            _set_block(block_enabled)
            while not stop_event.is_set():
                if is_finite and count >= limit_val:
                    break

                if pause_on_switch:
                    current_hwnd = self._get_foreground_hwnd()
                    if awaiting_target:
                        if current_hwnd is not None and current_hwnd != own_hwnd:
                            target_hwnd = current_hwnd
                            target_title = self._get_window_title(current_hwnd)
                            awaiting_target = False
                            _set_awaiting_target(False)
                        else:
                            _set_awaiting_target(True)
                            if not self._interruptible_sleep_event(0.2, stop_event):
                                break
                            continue
                    else:
                        if current_hwnd != target_hwnd:
                            switched = True
                        else:
                            switched = self._get_window_title(current_hwnd) != target_title
                        if switched:
                            _set_paused(True)
                            if not self._interruptible_sleep_event(0.2, stop_event):
                                break
                            continue
                _set_paused(False)

                if is_hold:
                    _keyboard_press(key_name)
                    held_ok = self._interruptible_sleep_event(
                        self.get_total_interval(self.press_hold_vars), stop_event)
                    _keyboard_release(key_name)
                    if not held_ok:
                        break
                else:
                    self._fire_presses(lambda: _keyboard_send(key_name), presses, stop_event)

                count += 1
                self.press_rate_counter.tick(1 if is_hold else presses)

                gap_ok = self._interruptible_sleep_event(
                    self.get_effective_interval(self.press_int_vars, max_speed, self.press_max_pps_entry),
                    stop_event)
                if not gap_ok:
                    break
        finally:
            if is_hold:
                try:
                    keyboard.release(key_name)
                except Exception:
                    pass
                for m in reversed(mod_keys):
                    try:
                        keyboard.release(m)
                    except Exception:
                        pass
            _set_block(False)
            self.presser_paused = False
            self.presser_awaiting_target = False
            if gen == self.presser_gen:
                self.presser_running = False
                self.presser_thread = None
                self._safe_ui_after(lambda: self._set_toggle_running_style(self.press_toggle_btn, False))
                self._safe_ui_after(lambda: self.refresh_toggle_button_label("press"))

    def _register_hotkey(self, which):
        spec = self.hotkey_specs.get(which)
        if spec is None:
            return
        hot = spec['entry'].get().strip().lower()
        old_handle = spec.get('registered_handle')
        if old_handle is not None:
            try:
                keyboard.remove_hotkey(old_handle)
            except Exception:
                pass
            spec['registered_handle'] = None
            spec['registered'] = None
        if hot and hot != "press a key...":
            try:
                handle = keyboard.add_hotkey(hot, (lambda cmd=spec['toggle']: self._safe_ui_after(cmd)))
                spec['registered_handle'] = handle
                spec['registered'] = hot
            except Exception:
                pass

    def _reregister_all_hotkeys(self):
        for which in list(self.hotkey_specs.keys()):
            self._register_hotkey(which)

    def listen_hotkeys(self):
        _INPUT_LIBS_READY.wait()
        self._reregister_all_hotkeys()

    def _trim_memory(self):
        gc.collect()
        if hasattr(ctypes, "windll"):
            try:
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                ctypes.windll.kernel32.SetProcessWorkingSetSize(handle, -1, -1)
            except Exception:
                pass

    def cleanup_idle_threads(self):
        for attr in ("clicker_thread", "presser_thread", "playback_thread"):
            th = getattr(self, attr, None)
            if th is not None and not th.is_alive():
                setattr(self, attr, None)
        self._trim_memory()

    def watch_memory(self):
        while True:
            time.sleep(300)
            try:
                if get_process_memory_mb() >= MEMORY_CLEANUP_THRESHOLD_MB:
                    self.cleanup_idle_threads()
            except Exception:
                pass

if __name__ == "__main__":
    if hasattr(ctypes, "windll"):
        try:
            ctypes.windll.winmm.timeBeginPeriod(1)
        except Exception:
            pass

    threading.Thread(target=_load_input_libs, daemon=True).start()

    root = tk.Tk()
    app = AutoClickerPresser(root)
    try:
        root.mainloop()
    finally:
        if hasattr(ctypes, "windll"):
            try:
                ctypes.windll.winmm.timeEndPeriod(1)
            except Exception:
                pass
