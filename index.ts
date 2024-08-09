import { input } from "@inquirer/prompts";

async function main() {
  while (true) {
    const answer = await input({ message: "Enter your name" });
    console.log(answer);
  }
}

main();
