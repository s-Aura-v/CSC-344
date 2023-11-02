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

let re_alphabet = Str.regexp "[A-Za-z0-9 .]+"  (* Make the regex case-insensitive *)
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
      let token = String.get s pos in
      (Tok_Char token)::(tok (pos + 1) s)
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

(*How to test:
   tokenize "abc"
   *)
(*Parser*)

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

  let match_tok a =
     match !tok_list with
    (* checks lookahead; advances on match *)
    | (h::t) when a = h -> tok_list := t
    | _ -> raise (ParseError "bad match")

  
    let rec parse_S () =
      let e = parse_E () in
      match lookahead () with
      | Tok_END -> e
      | _ -> raise (ParseError "S error")
    
    and parse_E () =
      let t = parse_T () in
      match lookahead () with
      | Tok_OR ->
        let _ = match_tok Tok_OR in
        let e = parse_E () in
        Alternation (t, e)
      | _ -> t
    
    and parse_T () =
      let f = parse_F () in
      match lookahead () with
      | Tok_Char _ | Tok_LPAREN ->
        let t = parse_T () in
        Concat (f, t)
      | _ -> f
    
    and parse_F () =
      let a = parse_A () in
      match lookahead () with
      | Tok_Q ->
        let _ = match_tok Tok_Q in
        Optional a
      | _ -> a
    
    and parse_A () =
      match lookahead () with
      | Tok_Char c ->
        let _ = match_tok (Tok_Char c) in
        C c
      | Tok_LPAREN ->
        let _ = match_tok Tok_LPAREN in
        let e = parse_E () in
        let _ = match_tok Tok_RPAREN in
        e
      | _ -> raise (ParseError "A error")
    
      let parse str =
        tok_list := (tokenize str);
        let exp = parse_S () in
        if !tok_list <> [Tok_END] then
          raise (ParseError "parse_S")
        else
          exp
       ;;
    


(*Matcher*)

let rec eval_pattern pattern str =
  let pos = ref 0 in
  let rec input_pattern pos = 
    let match pos with
  match pos with 
  | C c ->
    if (Char.equal str.[pos])

  | Concat(p1, p2) ->     
  
  | Optional p ->
  
  | Alternation(p1, p2) ->
    if 

      /


    

let pattern str =
  let ast = parse str in 
  fun input -> eval_pattern ast input 0;;

let string string = 
  let ast = string in
  fun input -> eval_pattern ast input 1;;












