# typed: true

# DO NOT EDIT MANUALLY
# This is an autogenerated file for dynamic methods in `Homebrew::DevCmd::Typecheck`.
# Please instead update this file by running `bin/tapioca dsl Homebrew::DevCmd::Typecheck`.


class Homebrew::DevCmd::Typecheck
  sig { returns(Homebrew::DevCmd::Typecheck::Args) }
  def args; end
end

class Homebrew::DevCmd::Typecheck::Args < Homebrew::CLI::Args
  sig { returns(T.nilable(String)) }
  def dir; end

  sig { returns(T.nilable(String)) }
  def file; end

  sig { returns(T::Boolean) }
  def fix?; end

  sig { returns(T.nilable(String)) }
  def ignore; end

  sig { returns(T::Boolean) }
  def suggest_typed?; end

  sig { returns(T::Boolean) }
  def update?; end

  sig { returns(T::Boolean) }
  def update_all?; end
end
