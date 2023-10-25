(*
S -: E$  
E -: C | EE | E'|'E | E'?' | '(' E ')'
C -: '0' | '1' | ... | '9'| 'a' | 'b' | ... | 'z' | '.'

 S  -: E$
 E  -: T '|' E | T
 T  -: F T | F
 F  -: A '?' | A
 A  -: C | '(' E ')'
 C  -: Alphanumeric characters plus '.'
*)


#directory "+str"
#load "str.cma"
open Str

(* Scanner Types *)
type token =
  | Tok_Char of char
  | Tok_OR
  | Tok_Q
  | Tok_LPAREN
  | Tok_RPAREN
  | Tok_END

let re_alphabet = Str.regexp "[A-Za-z0-9]+"  (* Make the regex case-insensitive *)
let re_or = Str.regexp "|"
let re_q = Str.regexp "?"
let re_lparen = Str.regexp "("
let re_rparen = Str.regexp ")"
(* Define a custom exception for parsing errors *)
exception ParseError of string

(* Tokenize the input regular expression string *)
let tokenize str =
  let rec tok pos s =
    if pos >= String.length s then
      [Tok_END]
    else if (Str.string_match re_alphabet s pos) then
      let token = Str.matched_string s in
      (Tok_Char (token.[0])) :: (tok (pos + (String.length token)) s)
    else if (Str.string_match re_or s pos) then
      Tok_OR :: (tok (pos + 1) s)
    else if (Str.string_match re_q s pos) then
      Tok_Q :: (tok (pos + 1) s)
    else if (Str.string_match re_lparen s pos) then
      Tok_LPAREN :: (tok (pos + 1) s)
    else if (Str.string_match re_rparen s pos) then
      Tok_RPAREN :: (tok (pos + 1) s)
    else
      raise (ParseError "tokenize")
  in
  tok 0 str

(* AST Types *)
type re =
  | C of char
  | Concat of re * re
  | Optional of re
  | Alternation of re * re

let tok_list = ref []



