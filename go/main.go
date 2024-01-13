package main

import (
	"bufio"
	"crypto"
	"crypto/hmac"
	"encoding/binary"
	"encoding/json"
	"flag"
	"fmt"
	"golang.org/x/crypto/scrypt"
	"golang.org/x/term"
	"os"
	"strings"
)

func main() {
	flags := parseFlags()
	config, err := readConfig()
	if err != nil {
		fmt.Printf("error reading config: %s\n", err.Error())
	}
	if flags.FullName == "" {
		if config.FullName != "" {
			flags.FullName = config.FullName
		} else {
			fullName, err := input("Full Name: ")
			if err != nil {
				fmt.Println(err.Error())
				os.Exit(1)
			}
			flags.FullName = fullName
		}
	}
	if flags.SiteName == "" {
		siteName, err := input("Site Name: ")
		if err != nil {
			fmt.Println(err.Error())
			os.Exit(1)
		}
		flags.SiteName = siteName
	}
	_, ok := TemplateDictionary[flags.SiteResultType]
	if !ok {
		typeAbbreviations := map[ResultType]ResultType{
			"x": "Maximum",
			"l": "Long",
			"m": "Medium",
			"b": "Basic",
			"s": "Short",
			"i": "PIN",
			"n": "Name",
			"p": "Phrase",
		}
		fullSiteResult, ok := typeAbbreviations[flags.SiteResultType]
		if !ok {
			fmt.Printf("Site result type not valid: %s\n", flags.SiteResultType)
			os.Exit(1)
		}
		flags.SiteResultType = ResultType(fullSiteResult)
	}
	fmt.Print("Password: ")
	pass, err := term.ReadPassword(int(os.Stdin.Fd()))
	fmt.Print("\n")
	if err != nil {
		fmt.Printf("password input error: %s\n", err.Error())
		os.Exit(1)
	}
	sitePassword, err := Password(flags.FullName, string(pass), flags.SiteName, flags.Counter, flags.SiteResultType)
	if err != nil {
		fmt.Printf("password generation error: %s\n", err.Error())
		os.Exit(1)
	}
	fmt.Printf("[ %s ]: %s\n",
		Identicon(flags.FullName, string(pass), true),
		sitePassword,
	)
}

func input(prompt string) (string, error) {
	fmt.Print(prompt)
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		return "", fmt.Errorf("An error occured while reading input. Please try again: %w", err)
	}
	return strings.TrimSuffix(input, "\n"), nil
}

type Config struct {
	FullName string `json:"FULL_NAME"`
}

func readConfig() (Config, error) {
	b, err := os.ReadFile(os.Getenv("HOME") + "/.config/mpw/config.json")
	if err != nil {
		return Config{}, err
	}
	var c Config
	err = json.Unmarshal(b, &c)
	if err != nil {
		return Config{}, err
	}
	return c, nil
}

type Flags struct {
	FullName       string
	Counter        int
	SiteResultType ResultType
	Verbose        bool
	Quiet          bool
	SiteName       string
}

func parseFlags() Flags {
	fullName := flag.String("full-name", "", "Specify the full name of the user, can be configured in json at " + os.Getenv("HOME") + "/.config/mpw/config.json")
	fullNameShorthand := flag.String("u", "", "Specify the full name of the user")
	counter := flag.Int("counter", 1, "Specify the full name of the user")
	counterShorthand := flag.Int("c", 1, "Specify the full name of the user")
	helpSiteResultType := "Specify the password's template\n" +
		"Defaults to 'long' (-t a)\n" +
		"x, Maximum  | 20 characters, contains symbols.\n" +
		"l, Long     | Copy-friendly, 14 characters, symbols.\n" +
		"m, Medium   | Copy-friendly, 8 characters, symbols.\n" +
		"b, Basic    | 8 characters, no symbols.\n" +
		"s, Short    | Copy-friendly, 4 characters, no symbols.\n" +
		"i, Pin      | 4 numbers.\n" +
		"n, Name     | 9 letter name.\n" +
		"p, Phrase   | 20 character sentence."
	siteResultType := flag.String("site-result-type", "Long", helpSiteResultType)
	siteResultTypeShortHand := flag.String("t", "Long", helpSiteResultType)
	verbose := flag.Bool("verbose", false, "Increase output verbosity")
	verboseShortHand := flag.Bool("v", false, "Increase output verbosity")
	quiet := flag.Bool("quiet", false, "Decrease output verbosity")
	quietShortHand := flag.Bool("q", false, "Decrease output verbosity")

	flag.Parse()

	if *fullNameShorthand != "" {
		fullName = fullNameShorthand
	}
	if *counterShorthand != 1 {
		counter = counterShorthand
	}
	if *siteResultTypeShortHand != "Long" {
		siteResultType = siteResultTypeShortHand
	}
	if *verboseShortHand {
		verbose = verboseShortHand
	}
	if *quietShortHand {
		quiet = quietShortHand
	}
	args := flag.Args()
	if len(args) > 1 {
		_, _ = fmt.Printf("only one non-flagged comman line argument allowed: %s", args)
		os.Exit(1)
	}
	siteName := ""
	if len(args) != 0 {
		siteName = args[0]
	}
	_ = fullName
	_ = counter
	_ = siteResultType
	_ = verbose
	_ = quiet
	_ = siteName
	return Flags{
		FullName:       *fullName,
		Counter:        *counter,
		SiteResultType: ResultType(*siteResultType),
		Verbose:        *verbose,
		Quiet:          *quiet,
		SiteName:       siteName,
	}
}

func Password(fullName, masterPassword, siteName string, siteCounter int, resultType ResultType) (string, error) {
	master, err := masterKey(masterPassword, fullName)
	if err != nil {
		return "", err
	}
	site, err := siteKey(siteName, master, uint(siteCounter))
	if err != nil {
		return "", err
	}
	return password(site, resultType)
}

func Identicon(fullName, masterPassword string, useColor bool) string {
	hash := hmac.New(crypto.SHA256.New, []byte(masterPassword))
	hash.Write([]byte(fullName))
	seed := hash.Sum(nil)
	leftArm := leftArms[seed[0]%byte(len(leftArms))]
	body := bodies[seed[1]%byte(len(bodies))]
	rightArm := rightArms[seed[2]%byte(len(rightArms))]
	accessory := accessories[seed[3]%byte(len(accessories))]
	color := colors[seed[4]%byte(len(colors))]
	icon := fmt.Sprintf("%s%s%s%s", leftArm, body, rightArm, accessory)
	if useColor {
		return fmt.Sprintf("%s%s%s", colorCodes[color], icon, colorCodes["White"])
	}
	return icon
}

// Phase 1: Your identity
//
//	Your identity is defined by your master key.  This key unlocks all of your
//	doors.  Your master key is the cryptographic result of two components:
//
//	1.Your <name> (identification)
//	2.Your <master password> (authentication)
//
//	Your master password is your personal secret and your name scopes that
//	secret to your identity.  Together, they create a cryptographic identifier
//	that is unique to your person.
//
//	´´´
//	masterKey = SCRYPT( key, seed, N, r, p, dkLen )
//	key = <master password>
//	seed = scope . LEN(<name>) . <name>
//	N = 32768
//	r = 8
//	p = 2
//	dkLen = 64
//	´´´
//
//	We employ the SCRYPT cryptographic function to derive a 64-byte
//	cryptographic key from the user’s name and master password using a fixed
//	set of parameters.
func masterKey(masterPassword string, name string) ([]byte, error) {
	lengthNameAsBytes := make([]byte, 4)
	binary.BigEndian.PutUint32(lengthNameAsBytes, uint32(len([]byte(name))))
	seed := []byte("com.lyndir.masterpassword")
	seed = append(seed, lengthNameAsBytes...)
	seed = append(seed, []byte(name)...)
	return scrypt.Key([]byte(masterPassword), seed, 32768, 8, 2, 64)
}

// Phase 2: Your site key "com.lyndir.masterpassword"
//
// Your site key is a derivative from your master key when it is used to
// unlock the door to a specific site. Your site key is the result of two
// components:
//
// 1.Your <site name> (identification)
// 2.Your <masterkey> (authentication)
// 3.Your <site counter>
//
// Your master key ensures only your identity has access to this key and your
// site name scopes the key to your site.  The site counter ensures you can
// easily create new keys for the site should a key become
// compromised. Together, they create a cryptographic identifier that is
// unique to your account at this site.
//
// siteKey = HMAC-SHA-256( key, seed )
// key = <master key>
// seed = scope . LEN(<site name>) . <site name> . <counter>
//
// We employ the HMAC-SHA-256 cryptographic function to derive a 64-byte
// cryptographic site key from the from the site name and master key scoped
// to a given counter value.
func siteKey(siteName string, masterKey []byte, counter uint) ([]byte, error) {
	lengthNameAsBytes := make([]byte, 4)
	binary.BigEndian.PutUint32(lengthNameAsBytes, uint32(len([]byte(siteName))))
	counterAsbytes := make([]byte, 4)
	binary.BigEndian.PutUint32(counterAsbytes, uint32(counter))
	seed := []byte("com.lyndir.masterpassword")
	seed = append(seed, lengthNameAsBytes...)
	seed = append(seed, []byte(siteName)...)
	seed = append(seed, counterAsbytes...)

	hash := hmac.New(crypto.SHA256.New, masterKey)
	_, err := hash.Write(seed)
	if err != nil {
		return nil, err
	}
	return hash.Sum(nil), nil
}

// Output Templates:
// In an effort to enforce increased password entropy, a common consensus has
// developed among account administrators that passwords should adhere to
// certain arbitrary password policies.  These policies enforce certain rules
// which must be honoured for an account password to be deemed acceptable.
//
// As a result of these enforcement practices, Master Password’s site key
// output must necessarily adhere to these types of policies.  Since password
// policies are governed by site administrators and not standardized, Master
// Password defines several password templates to make a best-effort attempt at
// generating site passwords that conform to these policies while also keeping
// its output entropy as high as possible under the constraints.
type ResultType string
type templaceCharacter rune
type template []templaceCharacter

var TemplateDictionary map[ResultType][]template = map[ResultType][]template{
	"Maximum": {
		{'a', 'n', 'o', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'},
		{'a', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'n', 'o'},
	},
	"Long": {
		{'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'n', 'o'},
		{'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'n', 'o'},
		{'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'n', 'o'},
		{'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'n', 'o'},
		{'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'v'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'n', 'o'},
		{'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'C', 'v', 'c', 'c', 'n', 'o'},
		{'C', 'v', 'c', 'c', 'n', 'o', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'n', 'o', 'C', 'v', 'c', 'c'},
		{'C', 'v', 'c', 'c', 'C', 'v', 'c', 'v', 'C', 'v', 'c', 'c', 'n', 'o'},
	},
	"Medium": {
		{'C', 'v', 'c', 'n', 'o', 'C', 'v', 'c'},
		{'C', 'v', 'c', 'C', 'v', 'c', 'n', 'o'},
	},
	"Short": {
		{'C', 'v', 'c', 'n'},
	},
	"Basic": {
		{'a', 'a', 'a', 'n', 'a', 'a', 'a', 'n'},
		{'a', 'a', 'n', 'n', 'a', 'a', 'a', 'n'},
		{'a', 'a', 'a', 'n', 'n', 'a', 'a', 'a'},
	},
	"PIN": {
		{'n', 'n', 'n', 'n'},
	},
	"Name": {{'c', 'v', 'c', 'c', 'v', 'c', 'v', 'c', 'v'}},
	"Phrase": {
		{'c', 'v', 'c', 'c', ' ', 'c', 'v', 'c', ' ', 'c', 'v', 'c', 'c', 'v', 'c', 'v', ' ', 'c', 'v', 'c'},
		{'c', 'v', 'c', ' ', 'c', 'v', 'c', 'c', 'v', 'c', 'v', 'c', 'v', ' ', 'c', 'v', 'c', 'v'},
		{'c', 'v', ' ', 'c', 'v', 'c', 'c', 'v', ' ', 'c', 'v', 'c', ' ', 'c', 'v', 'c', 'v', 'c', 'c', 'v'},
	},
}
var templateCharsDictionary map[templaceCharacter][]string = map[templaceCharacter][]string{
	'V': {"A", "E", "I", "O", "U"},
	'C': {"B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"},
	'v': {"a", "e", "i", "o", "u"},
	'c': {"b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"},
	'A': {"A", "E", "I", "O", "U", "B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"},
	'a': {"A", "E", "I", "O", "U", "a", "e", "i", "o", "u", "B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"},
	'n': {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"},
	'o': {"@", "&", "%", "?", ",", "=", "[", "]", "_", ":", "-", "+", "*", "$", "#", "!", "'", "^", "~", ";", "(", ")", "/", "."},
	'x': {"A", "E", "I", "O", "U", "a", "e", "i", "o", "u", "B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")"},
	' ': {" "},
}

// Phase 3: Your site password
// Your site password is an identifier derived from your site key in
// compoliance with the site’s password policy.
//
// The purpose of this step is to render the site’s cryptographic key into a
// format that the site’s password input will accept.
//
// Master Password declares several site password formats and uses these
// pre-defined password “templates” to render the site key legible.
//
// ´´´
// template = templates[ <site key>[0] % LEN( templates ) ]
//
// for i in 0..LEN( template )
//
//	passChars = templateChars[ template[i] ]2
//	passWord[i] = passChars[ <site key>[i+1] % LEN( passChars ) ]
//
// We resolve a template to use for the password from the site key’s first
// byte.  As we iterate the template, we use it to translate site key bytes
// into password characters.  The result is a site password in the form
// defined by the site template scoped to our site key.
//
// This password is then used to authenticate the user for his account at
// this site.
func password(siteKey []byte, class ResultType) (string, error) {
	templates, found := TemplateDictionary[class]
	if !found {
		return "", fmt.Errorf("class %s not found", class)
	}
	if len(templates) > 255 {
		return "", fmt.Errorf("template class %s to large, len %d but max 255", class, len(templates))
	}
	template := templates[uint8(siteKey[0])%uint8(len(templates))]
	if len(template) > len(siteKey) {
		return "", fmt.Errorf("template %s to large, len %d but max 255", class, len(template))
	}
	password := make([]string, 0)
	for i, tc := range template {
		passChars := templateCharsDictionary[tc]
		password = append(password,
			passChars[uint8(siteKey[i+1])%uint8(len(passChars))],
		)
	}
	return strings.Join(password, ""), nil
}

var leftArms = []string{"╔", "╚", "╰", "═"}
var rightArms = []string{"╗", "╝", "╯", "═"}
var bodies = []string{"█", "░", "▒", "▓", "☺", "☻"}
var accessories = []string{
	"◈", "◎", "◐", "◑", "◒", "◓", "☀", "☁", "☂", "☃", "", "★",
	"☆", "☎", "☏", "⎈", "⌂", "☘", "☢", "☣", "☕", "⌚", "⌛", "⏰",
	"⚡", "⛄", "⛅", "☔", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛",
	"♜", "♝", "♞", "♟", "♨", "♩", "♪", "♫", "⚐", "⚑", "⚔", "⚖",
	"⚙", "⚠", "⌘", "⏎", "✄", "✆", "✈", "✉", "✌"}

type color string
type colorCode string

var colorCodes = map[color]colorCode{
	"Red":     "\033[31m",
	"Green":   "\033[32m",
	"Yellow":  "\033[33m",
	"Blue":    "\033[34m",
	"Magenta": "\033[35m",
	"Cyan":    "\033[36m",
	"White":   "\033[37m",
}
var colors = []color{"Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"}
