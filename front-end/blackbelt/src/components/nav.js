import {
    Box,
    Flex,
    Avatar,
    Link,
    Button,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    MenuDivider,
    useDisclosure,
    useColorModeValue,
    Stack,
    HStack,
    useColorMode,
    Center,
    Image,
    Text
  } from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';
import ConnectWalletButton from "./connect"
  
  
export function Nav() {
// const { colorMode, toggleColorMode } = useColorMode();
// const { isOpen, onOpen, onClose } = useDisclosure();
return (
    <>
    {/* <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4}> */}
    <Box px={4}>
        <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
        <HStack spacing={8} alignItems={'center'}>
            <Image
                    // rounded={'lg'}
                    height={'48px'}
                    width={'48px'}
                    objectFit={'cover'}
                    src={'/favicon.png'}
                /> 
            <Box><Text fontSize={'xl'}><b>Blackbelt</b></Text></Box>
        </HStack>

        <Flex alignItems={'center'}>
            <Stack direction={'row'} spacing={7}>
              <ConnectWalletButton />
            </Stack>
        </Flex>
        </Flex>
    </Box>
    </>
);
}