import {
    Box,
    Container,
    Heading,
    SimpleGrid,
    Icon,
    Text,
    Stack,
    HStack,
    VStack,
    Button
  } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

const BACKEND_URL = "http://10.60.4.212:5000/"

export async function report () {
    var contract_address = document.getElementById("contract-address").value;
    // Call api for risk assessment
    const url = BACKEND_URL+'blacklist?contract_address='+contract_address;
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
    // update the report
    document.getElementById("reported").innerHTML = parseInt(document.getElementById("reported").innerHTML) + 1;
    // TODO grey out report button if already reported
    
})
}

export function Results() {
return (
    <Box p={4}>
    <Stack spacing={4} as={Container} maxW={'3xl'} textAlign={'center'}>
        <Heading fontSize={'3xl'}>Security Report:</Heading>
        <Text color={'gray.600'} fontSize={'xl'}>
            Contract Address: <span id="contract-address-out"></span>
            <br></br>
            Overall Risk level: <b><span id="risk-level"></span></b> 
            <br></br>
            Security Score: <b><span id="security-score"></span></b>
            <br></br>
        </Text>
    </Stack>
        <SimpleGrid columns={2} spacing={30} textAlign={'center'}>
            <Box color={'black.400'} height='40px' id="">
                {/* <CheckIcon color={'green.500'} /> */}
                <Text fontSize={'l'}>Source Code Verified on Etherscan?: <b><span id="verified"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Source Code Audited?: <b><span id="audited"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Contract Age (days): <b><span id="age"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Number of Transactions: <b><span id="transactions"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Number of Unique Users: <b><span id="users"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Number of Times Reported to Blackbelt: <b><span id="reported"></span></b></Text>
            </Box>
        </SimpleGrid>
    <Stack spacing={4} as={Container} maxW={'3xl'} textAlign={'center'}>
        <Button
                bg={'red.800'}
                color={'white'}
                type='submit'
                onClick={async () => await report()}
                _hover={{
                bg: 'red.500'
                }}>
                Report this contract
            </Button>
    </Stack>
    </Box>
);
}