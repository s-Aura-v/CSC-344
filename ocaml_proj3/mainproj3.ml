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

let re_alphabet = Str.regexp "[A-Za-z0-9 .]+"  (* Make the regex case-insensitive + add space and period *)
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

let rec eval_pattern pattern input pos =
  match pattern with
  | C c ->
    if pos < String.length input && (input.[pos] = c || c = '.') then
      Some (pos + 1)
    else
      None
  | Concat (p1, p2) ->
    begin
      match eval_pattern p1 input pos with
      | Some new_pos -> eval_pattern p2 input new_pos
      | None -> None
    end
  | Optional p ->
    begin
      match eval_pattern p input pos with
      | Some new_pos -> Some new_pos
      | None -> Some pos
    end
  | Alternation (p1, p2) ->
    let try_p1 = eval_pattern p1 input pos in
    if try_p1 <> None then
      try_p1
    else
      eval_pattern p2 input pos
;;

let match_pattern pattern input =
  match eval_pattern pattern input 0 with
  | Some pos when pos = String.length input -> print_endline "match"
  | _ -> print_endlines "no match"
;;

let pattern = "I (like|love|hate)( (cat|dog))? people"
let string = "2"

let pattern = parse pattern
let is_match = match_pattern pattern string



(*Test Inputs
let pattern = "I (like|love|hate)( (cat|dog))? people"
let string = "I like cat people"
let string = "I love dog people"
let string = "I hate people"
let string = "I likelovehate people"
let string = "I people"

let pattern = "((h|j)ell. worl?d)|(42)"
let string = "hello world"
let string = "jello word"
let string = "jelly word"
let string = "42"
let string = "24"
let string = "hello world42"
*)