#!/usr/bin/perl

 use utf8;

print $ARGV[0];

open(INPUT,$ARGV[0]) or die("\nErreur : non de fichier invalide\nUsage ./tocrfpp fichier_elttres_alignees\n");
open(OUTPUT,">$ARGV[0].crfpp") or die ("\nErreur: droit d'écriture dans le dossier\n");

use open ':encoding(utf8)';
binmode(INPUT, ":utf8");
binmode(OUTPUT, ":utf8");

#Limite de mot
my $j = 0;
$max = defined($ARGV[1])?$ARGV[1]:10000000;

while(<INPUT>) {
	if($j<$max) {
		
		my @strings = split(/\s/);


		for($i=0;$i<length($strings[0]);$i++){

			#On vérifie si Le fichier est un ensemble d'entrainement ou de test, traitement différent, car les fichiers de test contiennet des ... OR ...
			if (index($ARGV[1], "train") != -1) {
				print OUTPUT substr($strings[0],$i,1)." ".substr($strings[1],$i,1)."\n";
			}
			else{
				print OUTPUT substr($strings[0],$i,1)." _\n";
			}
		}
		print OUTPUT "\n";
		$j++;
	}

}

close INPUT;
close OUTPUT;
