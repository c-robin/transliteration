#!/usr/bin/perl

 use utf8;

open(RES,$ARGV[0]) or die("\nErreur : non de fichier invalide\nUsage ./res.pl fichier_resultats fichiers_test\n");
open(TEST,$ARGV[1]) or die("\nErreur : non de fichier invalide\nUsage ./res.pl fichier_resultats fichiers_test\n");


open(OUTPUT,">predicted.txt") or die ("\nErreur: droit d'écriture dans le dossier\n");

use open ':encoding(utf8)';
binmode(RES, ":utf8");
binmode(TEST, ":utf8");
binmode(OUTPUT, ":utf8");

my $nbtest=0;
my $correct=0;

#Array contenant les mots prédits par le CRF
@predictedwords;
#Vérité-terrain. Array contenant, poour chaque index, tous les mots corrects concaténés
@testwords;


while(<TEST>) {
	$words="";
	
	@strings = split(/\s/);
	
	for($i=1;$i<scalar(@strings);$i++) {
		if($strings[$i]=~/\#\w*\#/){
			$words= $words.$strings[$i];
		}
	}
	push(@testwords,$words);
}


$word = "";
while(<RES>) {
	my @strings = split(/\t/);
	

	if(@strings == 3) {
		#On rassemble les mots, en prenant soint d'ommettre les "_" qui sont des lettres vides
		if(!(substr($strings[2],0,1) eq "_")) {	
			$word = $word . substr($strings[2],0,1);
		}
	
	}
	#Fin d'un mot
	if(@strings == 1) {
		print OUTPUT $word."\n";
		push(@predictedwords,$word);
		$word ="";
	}
}

$nbtest = scalar(@predictedwords);

for($i=0;$i<@testwords;$i++) {
	if (index($testwords[$i], $predictedwords[$i]) != -1) {
		#Prediction bonne
		$correct++;
	}
	else
	{
		#rien, mais si on veut analyser les erreurs c'est ici
	}

}

$precision = $correct/$nbtest*100;

print "Nb éléments: ".$nbtest."\n";
print "Nb corrects: ".$correct."\n";
print "Précision : ". $precision ."%"."\n";

