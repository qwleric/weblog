#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <ctime>
#include <cstdlib>

using namespace std;

string to_lower(const string &s)
{
	string output = "";
	for(int i = 0, n = s.size(); i < n; ++i)
		output += tolower(s[i]);
	return output;
}

string readfile(const string &fn)
{
	/* thx jerry */
	std::ifstream t(fn);
	std::stringstream buffer;
	buffer << t.rdbuf();
	return buffer.str();
}

void fill_thesaurus(unordered_map<string, vector<string>> &thesaurus)
{
	string fn = "mobythesaurus.txt";
	ifstream fin(fn);
	if(fin.fail())
	{
		cout << "Unable to open thesaurus file\n";
		exit(1);
	}

	string s;
	while(getline(fin, s, '\r'))
	{
		istringstream ss(s);
		vector<string> synonyms = {};
		bool is_first = true;
		string word = "";
		while(getline(ss, s, ','))
		{
			if(is_first)
			{
				word = s;
				is_first = false;
				continue;
			}
			synonyms.push_back(s);
		}
		thesaurus[word] = synonyms;
	}
}

string replace_synonyms(unordered_map<string, vector<string>> &thesaurus, string message)
{
	unordered_set<string> blacklist = {"the", "of", "and", "to", "a", "in", "that", "is", "was", "he", "for", "it", "with", "as", "his", "on", "be", "at", "by", "i", "this", "had", "not", "are", "but", "from", "or", "have", "an", "they", "which", "one", "you", "were", "her", "she", "there", "would", "their", "we", "him", "been", "has", "when", "who", "will", "more", "no", "if", "out", "so", "what", "up", "its", "into", "than", "them", "can", "other", "new", "some", "could", "these", "two", "may", "then", "do", "first", "any", "my", "now", "such", "like", "our", "over", "me", "even", "most", "also", "did", "many", "must", "through", "back", "years", "way", "well", "should", "because", "each", "just", "those", "how", "too", "make", "see", "here", "both", "us"};
	string output = "";

	istringstream ss(message);
	string word;
	while(ss >> word)
	{
		word = to_lower(word);
		int r = rand() % 10;
		if(/*r >= 5 &&*/ blacklist.count(word) == 0 && thesaurus.count(word) > 0)
		{
			r = rand() % thesaurus[word].size();
			output += thesaurus[word][r] + " ";
		}
		else
			output += word + " ";
	}
	return output;
}

int main(int argc, char **argv)
{
	bool fromfile = false;
	string fn;
	if(argc != 2)
	{
		if(argc == 3)
		{
			string argv1 = argv[1];
			string argv2 = argv[2];
			if(argv1== "-f")
			{
				fromfile = true;
				fn = argv[2];
			}
			else if(argv2 == "-f")
			{
				fromfile = true;
				fn = argv[1];
			}
		}
		else {
			cout << "Usage: " << argv[0] << " message\n";
			return 1;
		}
	}

	srand(time(NULL));

	unordered_map<string, vector<string>> thesaurus;
	fill_thesaurus(thesaurus);
	string input = argv[1];
	if(fromfile) input = readfile(fn);
	string output = replace_synonyms(thesaurus, input);
	cout << output << endl;
}
