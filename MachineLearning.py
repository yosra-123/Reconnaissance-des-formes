

import presenters
import models
import views
import interactors


#----------------------------------------------------------------------------#
#																			 #
#								classe Main: 								 #
#							Debut du programme								 #
#																			 #
#----------------------------------------------------------------------------#

def main():
	presenters.PresenterShapeRecognition(
		model = models.ModelShapeRecognition,
		view = views.ViewShapeRecognition,
		interactor = interactors.InteractorShapeRecognition)

if __name__ == '__main__':
    main()
