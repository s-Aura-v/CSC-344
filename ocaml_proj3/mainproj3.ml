(*
S -: E$  
E -: C | EE | E'|'E | E'?' | '(' E ')'
C -: '0' | '1' | ... | '9'| 'a' | 'b' | ... | 'z' | '.
'*)

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

  let re_alphabet = Str.regexp "([A-Za-z0-9]+)"
  let re_or = Str.regexp "|"
  let re_q = Str.regexp "?"
  let re_lparen = Str.regexp "()"
  let re_rparen = Str.regexp ")"

  exception IllegalExpression of string

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
      raise (IllegalExpression "tokenize")
  in
  tok 0 str


(* ... (Parser) ... *)

(* AST Types *)
type re =
  | C of char
  | Concat of re * re
  | Optional of re
  | Alternation of re * re

let tok_list = ref []

exception ParseError of string

let lookahead () =
  match !tok_list with
    [] -> raise (ParseError "no tokens")
  | (h::t) -> h

let rec parse_OR () =
  let t = lookahead () in
  match t with
  | Tok_Char _ | Tok_LPAREN ->
    let e1 = parse_LParen () in
    let t' = lookahead () in
    (match t' with
     | Tok_OR ->
       match_tok Tok_OR;
       let e2 = parse_OR () in
       Alternation (e1, e2)
     | _ -> e1)
  | _ -> raise (ParseError "parse_OR")

and parse_LParen () =
  let f1 = parse_Q () in
  let t' = lookahead () in
  match t' with
  | Tok_Char _ | Tok_LPAREN ->
    let f2 = parse_Q () in
    Concat (f1, f2)
  | _ -> f1

and parse_Q () =
  let a = parse_A () in
  let t' = lookahead () in
  match t' with
  | Tok_Q ->
    match_tok Tok_Q;
    Optional a
  | _ -> a

and parse_A () =
  let t = lookahead () in
  match t with
  | Tok_Char c ->
    match_tok (Tok_Char c);
    C c
  | Tok_LPAREN ->
    match_tok Tok_LPAREN;
    let e = parse_E () in
    match_tok Tok_RPAREN;
    e
  | _ -> raise (ParseError "parse_A")



(*Interpreter*)
let parse_pattern pattern =
  tok_list := tokenize pattern;
  parse_E ()

let pattern_to_string pattern =
  let rec pattern_to_string_helper pattern =
    match pattern with
    | C c -> String.make 1 c
    | Concat (p1, p2) ->
      let str1 = pattern_to_string_helper p1 in
      let str2 = pattern_to_string_helper p2 in
      str1 ^ str2
    | Optional p -> "(" ^ pattern_to_string_helper p ^ ")?"
    | Alternation (p1, p2) ->
      let str1 = pattern_to_string_helper p1 in
      let str2 = pattern_to_string_helper p2 in
      "(" ^ str1 ^ "|" ^ str2 ^ ")"
  in
  pattern_to_string_helper pattern


(* Example usage *)
