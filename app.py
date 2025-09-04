#!/usr/bin/env python3
import aws_cdk as cdk
from sudoku_stack import SudokuStack

app = cdk.App()
SudokuStack(app, "SudokuStack")
app.synth()