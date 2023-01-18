import { isEthereumAddress, arrayToCsv, isPositiveInt } from "../../src/components/SendPoapDirect";

describe("utilities test", ()=>{
    test("aaa is not ethereum address",()=>{
        const result = isEthereumAddress("aaa");
    
        expect(result).toBe(false);
    });

    test("[['a']] is a, ", ()=>{
        const csv = arrayToCsv([['a']]);
        console.log("csv :", csv);

        expect(csv).toBe('"a"');
    });

    test("string -1 is not positive int", ()=>{
        const result = isPositiveInt('-1');

        expect(result).toBe(false);
    });


    test("string 0 is not positive int", ()=>{
        const result = isPositiveInt('0');

        expect(result).toBe(false);
    });

    test("string abc is not positive int", ()=>{
        const result = isPositiveInt('abc');

        expect(result).toBe(false);
    });

    test("string 1 is positive int", ()=>{
        const result = isPositiveInt('1');

        expect(result).toBe(true);
    });

    test("string 1.0 is not correct format positive int", ()=>{
        const result = isPositiveInt('1.0');

        expect(result).toBe(false);
    });

    test("string 1.1 is not positive int", ()=>{
        const result = isPositiveInt('1.1');

        expect(result).toBe(false);
    });

});

