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
  } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

// Replace test data with your own
// const features = Array.apply(null, Array(8)).map(function (x, i) {
// return {
//     id: i,
//     title: 'Lorem ipsum dolor sit amet',
//     text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam.',
// };
// });

export function Results() {
return (
    <Box p={4}>
    <Stack spacing={4} as={Container} maxW={'3xl'} textAlign={'center'}>
        <Heading fontSize={'3xl'}>Security Report:</Heading>
        <Text color={'gray.600'} fontSize={'xl'}>
            Overall Risk level: <b><span id="risk-level"></span></b> 
            <br></br>
            Security Score: <b><span id="security-score"></span></b>
            <br></br>
        </Text>
    </Stack>
        <SimpleGrid columns={2} spacing={30} textAlign={'left'}>
            <Box color={'black.400'} height='40px' id="">
                {/* <CheckIcon color={'green.500'} /> */}
                <Text fontSize={'l'}>Source Code Verified on Etherscan: <b><span id="verified"></span></b></Text>
            </Box>
            <Box color={'black.400'} height='40px'>
                <Text fontSize={'l'}>Source Code Audited: <b><span id="audited"></span></b></Text>
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
                <Text fontSize={'l'}>Number of Times Reported: <b><span id="reported"></span></b></Text>
            </Box>
        </SimpleGrid>
    </Box>
);
}