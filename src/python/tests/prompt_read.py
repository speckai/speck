from speck import Prompt

p = Prompt.read(path="prompts/test_one.prompt")
# print(p)

p2 = Prompt.read_all(path="prompts/test_many.prompt")
# print(p2)

Prompt.write(prompt=p2, path="prompts/test_write.prompt")
