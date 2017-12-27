import pandas as pd
import predictor
import os
import dropbox

class PreLoader:
	def __init__(self, path):
	################# required input files ###############
		print "#############"
		print "Root_Path: ", path
		print "###############"
        ############ required input instances ################
		self.predictor = predictor.MatPredidctor()
		self.dbx = dropbox.Dropbox('oXa01q2Xf-4AAAAAAAAFat8UzDzV7AkX-cBrN8coWKDcFK-ANG9HIF8P8g-MmdJy')
