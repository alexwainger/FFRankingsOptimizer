import csv
import sys, getopt

def main():
	with open('rankings/ActualRankings.csv', 'rb') as actual_f, open('rankings/BerryRankings.csv', 'rb') as berry_f, open('rankings/CockCroftRankings.csv', 'rb') as cc_f, open('rankings/KarabellRankings.csv', 'rb') as karabell_f, open('rankings/YatesRankings.csv', 'rb') as yates_f, open('picked_players.csv', 'rb') as picked_players_f:

		picked_players = set();
		pp_reader = csv.reader(picked_players_f);
		for line in pp_reader:
			picked_players.add(line[0]);

		actual_reader = csv.reader(actual_f);
		players = {};
		rank = 1;
		for line in actual_reader:
			player_obj = {
					"actual_rank": rank, 
					"name": line[0],
					"team": line[1].split()[0],
					"pos": line[1].split()[1]
					};

			players[line[0]] = player_obj;
			rank += 1;
		for f, rank_name in zip([berry_f, karabell_f, cc_f, yates_f], ["berry_rank", "karabell_rank", "cc_rank", "yates_rank"]):
			rank = 1;
			for line in csv.reader(f):
				name = line[0];
				if name in players:
					player_obj = players[name];
					player_obj[rank_name] = rank;
				rank += 1;

		player_list = [x for x in players.values() if "berry_rank" in x and "karabell_rank" in x and "cc_rank" in x and "yates_rank" in x];
		#sorted_list = sorted(player_list, key=lambda p: p["berry_rank"] if "berry_rank" in p else p["actual_rank"]);
		sorted_list = sorted(player_list, key=lambda p: p["berry_rank"] + p["karabell_rank"] + p["cc_rank"] + p["yates_rank"]);
		rank = 1;
		printed = 0;
		for el in sorted_list:
			if el["name"] not in picked_players:
				print str(rank) + ". " + " ".join([el["name"], str(el["actual_rank"]), str(float(el["actual_rank"]) - float(el["berry_rank"] + el["karabell_rank"] + el["cc_rank"] + el["yates_rank"]) / 4.0)]);
				printed += 1;
			rank += 1;

			if printed >= 20:
				break;


def pick_player(player_name):
	with open("picked_players.csv", "ab") as picked_players:
		writer = csv.writer(picked_players);
		writer.writerow([player_name]);

def print_rankings(ranking_name):
	with open("rankings/" + ranking_name + "Rankings.csv", "rb") as ranking_file, open("picked_players.csv", "rb") as picked_players_f:
		picked_players = set();
		pp_reader = csv.reader(picked_players_f);
		for line in pp_reader:
			picked_players.add(line[0]);

		rank = 1;
		count = 0;
		for line in csv.reader(ranking_file):
			if count > 20:
				break;
			if line[0] not in picked_players:
				print str(rank) + ". " + line[0];
				count += 1;

			rank += 1;

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "p:", ["picked=", "print="]);
	except getopt.GetoptError:
		print 'python processor.py [-p [--picked] <Played Picked>]';
		sys.exit(2);

	for opt, arg in opts:
		if opt in ("--print"):
			print arg + "'s Rankings:";
			print_rankings(arg);
		else:
			if opt in ("-p", "--picked"):
				pick_player(arg);

	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
	main();
