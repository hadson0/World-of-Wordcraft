PROMPT_TEMPLATE = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n## Instruction:\nWe are going to play a game called \"Infinite Craft\", Infinite Craft is a game like Little Alchemy but you can combine ANY element to possibly get a output!\nThe inputs to this game are the elements to be combined separated by comas.\nThe output will be the element that you get when combining the elements, (Either a new element or a existing element if it makes sense) or \"None\" if its impossible to combine the elements.\n \nFor example, combining Air and Earth might give us Stone. While combining Stone and Fire will give us Lava. However, Combining a element like Fire and Lava will give us None.\n\nSometimes the user will combine two of the same element. In some cases the output should be a bigger version of the element. For example, combining Water and Water might give us Ocean.\n \nElements can be combined in any order and some elements may have multiple leading combinations. (e.g., Mud can be created by combining Earth and Water, Earth and Rain or even Rain and Dirt).\n\nWhen outputting a response to a combination and the response is not \"None\" output JSON with the following format:\n\"Element_name\"\n\nExamples:\n \n- Input: \"Air, Earth\"\n- Output: \"Stone\"\n \n- Input: \"Water, Fire\"\n- Output: Steam\"\n \n- Input: \"Fire, Lava\"\n- Output: \"None\"\n \n*** IMPORTANT ***\nNEVER output more then 1 element at a time.\nMake sure to be creative but still logically correct!\n \nAir and Fire should not be equal to Lava.\nAir and Stone should be Sand. As the air would erode the stone.\nSand and Stone should not be Beach but rather Sandstone.\nSand and Mud should be Clay.\n \nOutputting \"[Element1], [Element2]\" as a element is not appropriate. Please provide a creative and logically correct response.\n \n*** VERRY IMPORTANT ***\nPLEASE avoid outputting esoteric or nonsensical responses such as MoltenGypsumGlassConcrete!!!\nDon't just combine words of the two elements. Try to combine the elements in a way that makes sense.\n \nThe response MUST and I mean MUST be just a single word.\nIf the combination is impossible the response MUST be \"None\".\nThe response MUST be simple and relatively short.\n\n### Input:\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"

ENCODING = "utf-8"

S_REGISTER = "registerRequest"
S_START_GAME = "startGame"
S_COMB_RESULT = "combResult"
S_GUESS_RESULT = "guessResult"
S_FINAL_SCORE = "finalScore"
S_LOBBY_CLOSED = "lobbyClosed"

C_NICKNAME = "nickname"
C_COMBINE = "combine"
C_GUESS = "guess"
C_STOP = "stop"
C_LEAVE = "leave"