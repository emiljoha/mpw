package main

import (
	"encoding/xml"
	"os"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestPassword(t *testing.T) {
	type TestID string
	type Test struct{
		Id TestID `xml:"id,attr"`
		Parent string `xml:"parent,attr"`
		Algorithm int `xml:"algorithm"`
		FullName string `xml:"fullName"`
		MasterPassword string `xml:"masterPassword"`
		KeyID string `xml:"keyID"`
		SiteName string `xml:"siteName"`
		SiteCounter int `xml:"siteCounter"`
		ResultType ResultType `xml:"resultType"`
		KeyPurpose string `xml:"keyPurpose"`
		Result string `xml:"result"`
		Identicon string `xml:"identicon"`
		KeyContext string `xml:"keyContext"`
	}
	var testDoc struct {
		Tests []Test `xml:"case"`
	}
	testcaseData, err :=os.ReadFile("testcases.xml")
	require.NoError(t, err)
	err = xml.Unmarshal(testcaseData, &testDoc)
	require.NoError(t, err)
	tests := make(map[TestID]Test, len(testDoc.Tests))
	for _, test := range testDoc.Tests {
		_, found := tests[test.Id]
		require.False(t, found, test.Id)
		tests[test.Id] = test
	}
	for _, test := range testDoc.Tests {
		if test.Parent == "" {
			continue
		}
		parent, found := tests[TestID(test.Parent)]
		require.True(t, found, test.Parent)
		if test.Algorithm == 0 {
			test.Algorithm = parent.Algorithm
		}
		if test.FullName == "" {
			test.FullName = parent.FullName
		}
		if test.MasterPassword == "" {			
			test.MasterPassword = parent.MasterPassword
		}
		if test.KeyID == "" {			
			test.KeyID = parent.KeyID
		}
		if test.SiteName == "" {			
			test.SiteName = parent.SiteName
		}
		if test.SiteCounter == 0 {			
			test.SiteCounter = parent.SiteCounter
		}
		if test.ResultType == "" {			
			test.ResultType = parent.ResultType
		}
		if test.KeyPurpose == "" {			
			test.KeyPurpose = parent.KeyPurpose
		}
		if test.Result == "" {
			test.Result    =   parent.Result
		}
		if test.Identicon == "" {
			test.Identicon =  parent.Identicon 			
		}
		if test.KeyContext == "" {
			test.KeyContext =  parent.KeyContext 			
		}
		tests[test.Id] = test
	}
	for id, test := range tests {
		if test.Algorithm != 3 {
			continue
		}
		if test.KeyContext != "" {
			continue
		}
		if test.KeyPurpose != "Authentication" {
			continue
		}
		t.Run(string(id), func(t *testing.T) {
			passwd, err := Password(
				test.FullName, test.MasterPassword, test.SiteName, test.SiteCounter, test.ResultType,
			)
			require.NoError(t, err)
			require.Equal(t, test.Result, passwd)
		})
	}
}


