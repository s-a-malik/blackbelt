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
import { FaBorderNone } from 'react-icons/fa';

const BACKEND_URL = "http://127.0.0.1:5000/"

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
    // document.getElementById("score").innerHTML = data.score;
    })
}

export function SimpleCard() {
return (
    <Flex
    minH={'100vh'}
    align={'center'}
    justify={'center'}
    bg={useColorModeValue('gray.50', 'gray.800')}>
    <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
        <Heading fontSize={'4xl'}>Test it out yourself!</Heading>
        <Text fontSize={'lg'} color={'gray.600'}>
            Enter a contract address below <br></br> to gain security insights 🔥🔥
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
                bg={'blue.400'}
                color={'white'}
                type='submit'
                onClick={async () => await getSecurityScore()}
                _hover={{
                bg: 'blue.500'
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