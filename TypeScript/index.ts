import {SquareConfig} from "./SquareConfig"

function createSquare(config: SquareConfig): { color: string; area: number } {
  let newSquare = {
    color: "white",
    area: 100
  }

  if (config.color) {
    newSquare.color = config.color
  }

  if (config.width) {
    newSquare.area = config.width * config.width
  }

  return newSquare
}
   
let mySquare = createSquare({ color: "black" })
console.log(mySquare.color)

//linha adicionada em feature/javascript