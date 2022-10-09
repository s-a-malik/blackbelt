import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    Checkbox,
    Stack,
    Link,
    Button,
    Heading,
    Text,
    useColorModeValue,
  } from '@chakra-ui/react';
import { FaBorderNone, FaDigitalTachograph } from 'react-icons/fa';

// const BACKEND_URL = "http://127.0.0.1:5000/"
const BACKEND_URL = "http://10.60.4.212:5000/"

export async function getSecurityScore () {
    var contract_address = document.getElementById("contract-address").value;
    var chain_id = document.getElementById("chain-id").value;
    // Call api for risk assessment
    const url = BACKEND_URL+'security_score?contract_address='+contract_address+'&chain='+chain_id;
    console.log(url);
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
  
    headers.append('Access-Control-Allow-Origin', 'http://localhost:3000');
    headers.append('Access-Control-Allow-Credentials', 'true');
  
    headers.append('GET', 'POST', 'OPTIONS');
    await fetch(url, {method: 'GET', headers: {
        'Content-Type': 'application/json'
      }})
    .then((response) => response.json())
    .then((data) => {
    console.log(data);
    if (data.status != "ok") {
        alert(data.status);
    }
    else {
        // fill in the security report
        document.getElementById("contract-address-out").innerHTML = contract_address;
        document.getElementById("risk-level").innerHTML = data.risk_level;
        document.getElementById("security-score").innerHTML = data.security_score;
        if (data.risk_level == "High") {
            document.getElementById("risk-level").style.color = "red";
        }
        else if (data.risk_level == "Medium") {
            document.getElementById("risk-level").style.color = "orange";
        }
        else if (data.risk_level == "Low") {
            document.getElementById("risk-level").style.color = "green";
        }
        document.getElementById("audited").innerHTML = data.contract_info.audited;
        document.getElementById("verified").innerHTML = data.contract_info.verified;
        document.getElementById("age").innerHTML = data.contract_info.min_age_of_contract_in_days;
        document.getElementById("transactions").innerHTML = data.contract_info.number_of_transactions;
        document.getElementById("users").innerHTML = data.contract_info.number_of_unique_users;
        document.getElementById("reported").innerHTML = data.num_times_reported;
    }
})
}

export function SimpleCard() {
return (
    <Flex
    minH={'10vh'}
    align={'center'}
    justify={'center'}
    bg={useColorModeValue('gray.50', 'gray.800')}>
    <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
        <Heading fontSize={'4xl'}>Blackbelt - self-defence for web3 scams</Heading>
        <Text fontSize={'lg'} color={'gray.600'}>
            Blackbelt is a tool to help you assess the real-time security of a smart contract before interacting with it. <br></br> 
            Try it below!
        </Text>
        </Stack>
        <Box
        rounded={'lg'}
        bg={useColorModeValue('white', 'gray.700')}
        boxShadow={'lg'}
        p={8}>
        <Stack spacing={4}>
            <FormControl id="contract-address">
            <FormLabel>Contract Address</FormLabel>
            <Input type="contract-address" />
            </FormControl>
            <FormControl id="chain-id">
            <FormLabel>Chain ID</FormLabel>
            <Input type="chain-id" />
            </FormControl>
            <Stack spacing={10}>
            <Button
                bg={'purple.400'}
                color={'white'}
                type='submit'
                onClick={async () => await getSecurityScore()}
                _hover={{
                bg: 'purple.600'
                }}>
                Rate now
            </Button>
            </Stack>
        </Stack>
        </Box>
    </Stack>
    </Flex>
);
}